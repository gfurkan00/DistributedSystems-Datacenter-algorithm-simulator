from typing import List, Dict, Any

from .utils import PendingProposal, PreparePayload, PromisePayload, AcceptPayload
from src.core.node.node import Node
from src.core.network import NetworkAPI
from src.core.utils import Message, MessageType, ClientRequestPayload, ClientResponsePayload, Status
from src.core.oracles import OracleLeader


class ProposerNode(Node):
    def __init__(self, node_id: int, network: NetworkAPI, settings: Dict[str, Any]):
        super().__init__(node_id, network)
        self._acceptor_ids: List[int] = settings.get("acceptor_ids", [])
        if not self._acceptor_ids:
            raise ValueError("Acceptor ids must be specified")

        self._pending: Dict[str, PendingProposal] = {}
        self._next_proposal_number: int = node_id + 1
        self._proposal_step: int = len(self._acceptor_ids) + 1
        self._majority = (len(self._acceptor_ids) // 2) + 1

        OracleLeader.register_leader(self._node_id)

    def receive(self, msg: Message):
        if not self.is_alive:
            return

        if msg.msg_type == MessageType.CLIENT_REQUEST:
            self._handle_client_request(msg=msg)

        elif msg.msg_type == MessageType.PROMISE:
            self._handle_promise(msg=msg)

        elif msg.msg_type == MessageType.ACCEPTED:
            self._handle_accepted(msg=msg)

    def _handle_client_request(self, msg: Message):
        client_payload: ClientRequestPayload = msg.payload
        request_id = client_payload.request_id
        client_id = msg.src_id
        value = client_payload.data

        proposal_number = self._next_proposal_number
        self._next_proposal_number += self._proposal_step

        self._pending[request_id] = PendingProposal(
            client_id=client_id,
            request_id=request_id,
            value=value,
            proposal_number=proposal_number
        )

        payload: PreparePayload = PreparePayload(request_id=request_id, proposal_number=proposal_number)
        for acc_id in self._acceptor_ids:
            self.send(acc_id, MessageType.PREPARE, payload)

    def _handle_promise(self, msg: Message):
        payload: PromisePayload = msg.payload
        request_id = payload.request_id
        proposal_number = payload.proposal_number

        if request_id not in self._pending:
            return

        state = self._pending[request_id]

        if proposal_number != state.proposal_number:
            return

        if msg.src_id in state.promises_from:
            return

        state.promises_from.add(msg.src_id)

        last_accepted_proposal_number = payload.last_accepted_proposal_number
        last_accepted_value = payload.last_accepted_value

        if last_accepted_proposal_number is not None and last_accepted_value is not None:
            if last_accepted_proposal_number > state.highest_seen_accepted_proposal_number:
                state.highest_seen_accepted_proposal_number = last_accepted_proposal_number
                state.value = last_accepted_value


        if len(state.promises_from) >= self._majority and not state.phase2_started:
            state.phase2_started = True

            accept_payload: AcceptPayload = AcceptPayload(
                request_id=state.request_id,
                proposal_number=state.proposal_number,
                value=state.value,
            )

            for acc_id in self._acceptor_ids:
                self.send(acc_id, MessageType.ACCEPT, accept_payload)

    def _handle_accepted(self, msg: Message):
        payload: AcceptPayload = msg.payload
        request_id = payload.request_id
        proposal_number = payload.proposal_number

        if request_id not in self._pending:
            return

        state = self._pending[request_id]
        if proposal_number != state.proposal_number:
            return

        state.accepted_from.add(msg.src_id)

        if len(state.accepted_from) >= self._majority and not state.committed:
            state.committed = True

            response_payload: ClientResponsePayload = ClientResponsePayload(
                request_id=request_id,
                status=Status.SUCCESS,
            )

            self.send(state.client_id, MessageType.CLIENT_RESPONSE, response_payload)