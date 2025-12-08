
from typing import Any, Dict

from src.core.node.node import Node
from src.core.network import NetworkAPI
from src.core.utils import Message, MessageType


class AcceptorNode(Node):
    """Basic single‑instance Paxos acceptor.

    Each distinct client request (identified by `request_id`) is treated
    as a separate Paxos instance.
    """

    def __init__(self, node_id: int, network: NetworkAPI):
        super().__init__(node_id, network)
        # For each request_id we track the highest promise and any value accepted.
        self._promised_n: Dict[str, int] = {}
        self._accepted_n: Dict[str, int] = {}
        self._accepted_value: Dict[str, Any] = {}

    def receive(self, msg: Message):
        if msg.msg_type == MessageType.PREPARE:
            self._handle_prepare(msg)
        elif msg.msg_type == MessageType.ACCEPT:
            self._handle_accept(msg)
        # Other message types are ignored by acceptors.

    # ------------------------------------------------------------------ #
    # Internal handlers                                                   #
    # ------------------------------------------------------------------ #
    def _handle_prepare(self, msg: Message) -> None:
        payload = msg.payload
        request_id: str = payload["request_id"]
        n: int = payload["n"]

        promised = self._promised_n.get(request_id, -1)
        if n <= promised:
            # Already promised a higher proposal number – ignore.
            return

        # Update promise
        self._promised_n[request_id] = n

        last_accepted_n = self._accepted_n.get(request_id)
        last_accepted_value = self._accepted_value.get(request_id)

        promise_payload = {
            "request_id": request_id,
            "n": n,
            "last_accepted_n": last_accepted_n,
            "last_accepted_value": last_accepted_value,
        }
        # Reply with PROMISE to the proposer that sent PREPARE
        self.send(msg.src_id, MessageType.PROMISE, promise_payload)

    def _handle_accept(self, msg: Message) -> None:
        payload = msg.payload
        request_id: str = payload["request_id"]
        n: int = payload["n"]
        value = payload["value"]

        promised = self._promised_n.get(request_id, -1)
        if n < promised:
            # We already promised not to accept proposal numbers below `promised`.
            return

        # Accept this proposal.
        self._promised_n[request_id] = n
        self._accepted_n[request_id] = n
        self._accepted_value[request_id] = value

        accepted_payload = {
            "request_id": request_id,
            "n": n,
            "value": value,
        }
        self.send(msg.src_id, MessageType.ACCEPTED, accepted_payload)
