from src.core.node.node import Node
from src.core.network import NetworkAPI
from src.core.utils import Message, MessageType
from src.protocols.primary_backup.utils import ReplicationPayload


class BackupNode(Node):
    def __init__(self, node_id: int, network: NetworkAPI):
        super().__init__(node_id, network)

    def receive(self, message: Message):
        if not self.is_alive:
            return

        if message.msg_type == MessageType.REPLICATION:
            self._handle_replication_request(message=message)

    def _handle_replication_request(self, message: Message):
        replication_payload: ReplicationPayload = message.payload
        request_id = replication_payload.request_id
        data = replication_payload.payload

        print(f"Backup node {self._node_id} get replication request from primary node {message.src_id} for the payload {data}")

        self.send(message.src_id, MessageType.ACK, request_id)
