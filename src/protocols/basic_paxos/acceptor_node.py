from typing import Any, Dict

from src.core.node.node import Node
from src.core.network import NetworkAPI
from src.core.utils import Message, MessageType
from src.protocols.basic_paxos.utils import PreparePayload, PromisePayload, AcceptPayload


class AcceptorNode(Node):
    def __init__(self, node_id: int, network: NetworkAPI):
        super().__init__(node_id, network)
        self._promised_proposals_number: Dict[str, int] = {}
        self._accepted_proposals_number: Dict[str, int] = {}
        self._accepted_value: Dict[str, Any] = {}

    def receive(self, msg: Message):
        if not self.is_alive:
            return

        if msg.msg_type == MessageType.PREPARE:
            self._handle_prepare(msg)
        elif msg.msg_type == MessageType.ACCEPT:
            self._handle_accept(msg)


    def _handle_prepare(self, msg: Message) -> None:
        payload: PreparePayload = msg.payload
        request_id = payload.request_id
        proposal_number = payload.proposal_number

        promised = self._promised_proposals_number.get(request_id, -1)
        if proposal_number <= promised:
            return

        self._promised_proposals_number[request_id] = proposal_number

        last_accepted_proposal_number = self._accepted_proposals_number.get(request_id)
        last_accepted_value = self._accepted_value.get(request_id)

        promise_payload: PromisePayload = PromisePayload(
            request_id=request_id,
            proposal_number=proposal_number,
            last_accepted_proposal_number=last_accepted_proposal_number,
            last_accepted_value=last_accepted_value,
        )
        self.send(msg.src_id, MessageType.PROMISE, promise_payload)

    def _handle_accept(self, msg: Message) -> None:
        payload: AcceptPayload = msg.payload
        request_id = payload.request_id
        proposal_number = payload.proposal_number
        value = payload.value

        promised = self._promised_proposals_number.get(request_id, -1)
        if proposal_number < promised:
            return

        self._promised_proposals_number[request_id] = proposal_number
        self._accepted_proposals_number[request_id] = proposal_number
        self._accepted_value[request_id] = value

        accepted_payload: AcceptPayload = AcceptPayload(
            request_id=request_id,
            proposal_number=proposal_number,
            value=value,
        )
        self.send(msg.src_id, MessageType.ACCEPTED, accepted_payload)
