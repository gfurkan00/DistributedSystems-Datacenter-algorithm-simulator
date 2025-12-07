from typing import List, Dict, Any

from src.core.node.node import Node
from src.core.network import NetworkAPI
from src.core.utils import Message, MessageType, ClientResponsePayload, Status, Oracle, ClientRequestPayload
from src.protocols.primary_backup.utils import PendingRequest, ReplicationPayload


class PrimaryNode(Node):
    def __init__(self, node_id: int, network: NetworkAPI, settings: Dict[str, Any]):
        super().__init__(node_id, network)
        self._backup_ids: List[int] = settings.get('backup_ids', [])
        if not self._backup_ids:
            raise ValueError(f"PrimaryNode {self._node_id} initialized without backup ids list!")

        self._replication_factor = settings.get(
            "replication_factor",
            max(1, len(self._backup_ids) // 2)
        )

        self._pending_request_dict: Dict[str, PendingRequest] = {}

        Oracle.set_leader_id(self._node_id)

    def receive(self, message: Message):
        if not self.is_alive:
            return

        if message.msg_type == MessageType.CLIENT_REQUEST:
            self._handle_client_request(msg=message)

        elif message.msg_type == MessageType.ACK:
            self._handle_ack_response(message=message)

    def _handle_client_request(self, msg: Message):
        client_payload: ClientRequestPayload = msg.payload
        self._pending_request_dict[client_payload.request_id] = PendingRequest(request_id=client_payload.request_id, client_id=msg.src_id, acks=set())
        replication_payload = ReplicationPayload(request_id=client_payload.request_id, payload=msg.payload)
        self._broadcast_replication(replication_payload=replication_payload)

    def _broadcast_replication(self, replication_payload: ReplicationPayload):
        for backup_id in self._backup_ids:
            self.send(backup_id, MessageType.REPLICATION, replication_payload)


    def _handle_ack_response(self, message: Message):
        request_id = message.payload
        backup_id = message.src_id

        if request_id not in self._pending_request_dict:
            return

        pending_request = self._pending_request_dict[request_id]
        pending_request.acks.add(backup_id)

        if len(pending_request.acks) >= self._replication_factor:
            client_id = pending_request.client_id
            response_payload: ClientResponsePayload = ClientResponsePayload(request_id=request_id, status=Status.SUCCESS)
            self.send(dst_id=client_id, msg_type=MessageType.CLIENT_RESPONSE, payload=response_payload)

            del self._pending_request_dict[request_id]