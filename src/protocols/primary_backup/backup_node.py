from src.core.node.node import Node
from src.core.network import NetworkAPI
from src.core.utils import Message, MessageType
from src.protocols.primary_backup.utils import ReplicationPayload


class BackupNode(Node):
    def __init__(self, node_id: int, network: NetworkAPI):
        super().__init__(node_id, network)

    def receive(self, msg: Message):
        if msg.msg_type == MessageType.REPLICATION:
            replication_payload: ReplicationPayload = msg.payload
            request_id = replication_payload.request_id
            data = replication_payload.payload

            print(f"Backup node {self._node_id} get replication request from primary node {msg.src_id} for the payload {data}")

            self.send(msg.src_id, MessageType.ACK, request_id)