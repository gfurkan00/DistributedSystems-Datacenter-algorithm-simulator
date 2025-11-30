
from .node import Node
from src.core.network import NetworkAPI
from src.core.utils import Message, MessageType, ClientResponsePayload


class ClientNode(Node):
    def __init__(self, node_id: int, network: NetworkAPI):
        super().__init__(node_id, network)

    def receive(self, msg: Message):
        if msg.msg_type == MessageType.CLIENT_RESPONSE:
            payload: ClientResponsePayload = msg.payload
            print(f"Client node {self._node_id} receive response from node {msg.src_id}, with payload {payload}")