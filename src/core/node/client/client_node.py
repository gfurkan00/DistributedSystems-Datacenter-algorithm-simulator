from typing import Dict, Any

from src.core.network import NetworkAPI
from src.core.node import Node
from src.core.utils import Message, MessageType, ClientResponsePayload

class ClientNode(Node):
    def __init__(self, node_id: int, network: NetworkAPI, settings: Dict[str, Any]):
        super().__init__(node_id, network)
        self._total_requests_to_do: int = settings.get('num_requests_per_client')
        if self._total_requests_to_do is None:
            raise ValueError('Total request to do must be greater than 0')

        self._loop_client_period = settings.get('loop_client_period', 1)

        self._requests_already_sent: int = 0

        self._schedule_next_loop_tick()

    def receive(self, msg: Message):
        if msg.msg_type == MessageType.CLIENT_LOOP:
            self._handle_client_loop()

        elif msg.msg_type == MessageType.CLIENT_RESPONSE:
            self._handle_client_response(msg=msg)


    def _handle_client_loop(self):
        print("handle client loop")

        self._schedule_next_loop_tick()

    def _handle_client_response(self, msg: Message):
        payload: ClientResponsePayload = msg.payload
        print(f"Client node {self._node_id} receive response from node {msg.src_id}, with payload {payload}")


    def _schedule_next_loop_tick(self):
        self.send_sync(dst_id=self._node_id, msg_type=MessageType.CLIENT_LOOP, payload=None, sync_latency=self._loop_client_period, violation_probability=0.0)