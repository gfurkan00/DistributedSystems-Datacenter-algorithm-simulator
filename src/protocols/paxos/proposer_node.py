from typing import List, Dict

from src.core.node.node import Node
from src.core.network import NetworkAPI
from src.core.utils import Message, MessageType
from src.protocols.paxos.utils import PendingProposal


class ProposerNode(Node):
    def __init__(self, node_id: int, network: NetworkAPI, acceptor_ids: List[int]):
        super().__init__(node_id, network)
        self._acceptor_ids: List[int] = acceptor_ids
        self._pending: Dict[str, PendingProposal] = {}
        self._next_proposal_number: int = 1

    def receive(self, msg: Message):
        # STEP 1: handle client requests – start Paxos
        if msg.msg_type == MessageType.CLIENT_REQUEST:
            request_id = msg.id
            client_id = msg.src_id
            value = msg.payload

            # new proposal number
            n = self._next_proposal_number
            self._next_proposal_number += 1

            # remember state
            self._pending[request_id] = PendingProposal(
                client_id=client_id,
                value=value,
                proposal_number=n,
                promises_from=set(),
                accepted_from=set(),
            )

            # send PREPARE to all acceptors
            for acc_id in self._acceptor_ids:
                payload = {"request_id": request_id, "n": n}
                self.send(acc_id, MessageType.PREPARE, payload)

        # STEP 2: handle PROMISE
        elif msg.msg_type == MessageType.PROMISE:
            payload = msg.payload
            request_id = payload["request_id"]
            n = payload["n"]

            if request_id not in self._pending:
                return

            state = self._pending[request_id]
            if n != state.proposal_number:
                return  # old promise, ignore

            state.promises_from.add(msg.src_id)

            last_n = payload["last_accepted_n"]
            last_val = payload["last_accepted_value"]
            if last_n is not None and last_val is not None:
                # adopt value that was already accepted
                state.value = last_val

            # majority of PROMISEs → send ACCEPT
            if len(state.promises_from) >= (len(self._acceptor_ids) // 2 + 1):
                for acc_id in self._acceptor_ids:
                    accept_payload = {
                        "request_id": request_id,
                        "n": state.proposal_number,
                        "value": state.value,
                    }
                    self.send(acc_id, MessageType.ACCEPT, accept_payload)

        # STEP 3: handle ACCEPTED
        elif msg.msg_type == MessageType.ACCEPTED:
            payload = msg.payload
            request_id = payload["request_id"]
            n = payload["n"]

            if request_id not in self._pending:
                return

            state = self._pending[request_id]
            if n != state.proposal_number:
                return

            state.accepted_from.add(msg.src_id)

            # majority of ACCEPTED → reply to client
            if len(state.accepted_from) >= (len(self._acceptor_ids) // 2 + 1):
                client_id = state.client_id
                response_payload = {
                    "request_id": request_id,
                    "status": "committed",
                    "value": state.value,
                }
                self.send(client_id, MessageType.CLIENT_RESPONSE, response_payload)
                del self._pending[request_id]
