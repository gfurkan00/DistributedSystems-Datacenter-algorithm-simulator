from typing import List, Dict

from src.core.node.node import Node
from src.core.network import NetworkAPI
from src.core.utils import Message, MessageType, ClientResponsePayload, Status
from src.protocols.primary_backup.utils import PendingRequest, ReplicationPayload


class PrimaryNode(Node):
    def __init__(self, node_id: int, network: NetworkAPI, backup_ids: List[int]):
        super().__init__(node_id, network)
        self._backup_ids: List[int] = backup_ids
        self._pending_request_dict: Dict[str, PendingRequest] = {}

    def receive(self, msg: Message):
        if msg.msg_type == MessageType.CLIENT_REQUEST:
            self._pending_request_dict[msg.id] = PendingRequest(client_id=msg.src_id, acks=set())
            replication_payload = ReplicationPayload(request_id=msg.id, payload=msg.payload)

            for backup_id in self._backup_ids:
                self.send(backup_id, MessageType.REPLICATION, replication_payload)

        elif msg.msg_type == MessageType.ACK:
            request_id = msg.payload
            backup_id = msg.src_id

            if request_id not in self._pending_request_dict:
                return

            pending_request = self._pending_request_dict[request_id]
            pending_request.acks.add(backup_id)

            if len(pending_request.acks) >= len(self._backup_ids):
                client_id = pending_request.client_id
                response_payload: ClientResponsePayload = ClientResponsePayload(request_id=request_id, status=Status.SUCCESS)
                self.send(client_id, MessageType.CLIENT_RESPONSE, response_payload)

                del self._pending_request_dict[request_id]