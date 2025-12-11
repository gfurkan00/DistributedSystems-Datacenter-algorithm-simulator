from typing import Dict, Any

from src.core.network import NetworkAPI
from src.core.node import Node
from .utils import PendingRequestState
from src.core.utils import Message, MessageType, ClientResponsePayload, MessageFactory, new_uuid, \
    ClientRequestPayload, Status
from src.core.oracles import OracleRequest, OracleLeader


class ClientNode(Node):
    def __init__(self, node_id: int, network: NetworkAPI, settings: Dict[str, Any]):
        super().__init__(node_id, network)
        self._total_requests_to_send: int = settings.get('num_requests_per_client')
        if self._total_requests_to_send is None:
            raise ValueError('Total request to send must be greater than 0')

        self._pending_requests: Dict[str, PendingRequestState] = {}

        self._loop_client_period = settings.get('loop_client_period', 1)
        self._request_timeout_period = settings.get('request_timeout_period', 2.5)
        self._retry_count = settings.get('retry_count', 3)

        self._requests_generated_count: int = 0
        self._schedule_next_loop_tick()

    def receive(self, message: Message):
        if not self.is_alive:
            return

        if message.msg_type == MessageType.INTERNAL_LOOP:
            self._handle_client_loop()

        elif message.msg_type == MessageType.TIMEOUT_CHECK:
            self._handle_request_timeout(request_id=message.payload)

        elif message.msg_type == MessageType.CLIENT_RESPONSE:
            self._handle_client_response(message=message)

    def _handle_client_loop(self):
        request_id = new_uuid()
        payload = f"Client_{self.node_id}_Req_{self._requests_generated_count}"

        request_state = PendingRequestState(
            request_id=request_id,
            payload_data=payload,
            retries_left=self._retry_count
        )
        self._pending_requests[request_id] = request_state
        self._execute_send_attempt(request_id=request_id)
        self._requests_generated_count += 1
        if self._requests_generated_count < self._total_requests_to_send:
            self._schedule_next_loop_tick()
        else:
            print(f"Client {self.node_id} Completed generation phase")

    def _execute_send_attempt(self, request_id: str):
        state = self._pending_requests.get(request_id)
        if not state:
            return

        target_id = OracleLeader.get_leader_id()
        payload = ClientRequestPayload(
            request_id=state.request_id,
            data=state.payload_data
        )
        msg = MessageFactory.build_message(
            src_id=self._node_id,
            dst_id=target_id,
            msg_type=MessageType.CLIENT_REQUEST,
            payload=payload
        )
        self._network.send(message=msg)
        self._schedule_next_request_timeout(request_id=request_id)

    def _handle_request_timeout(self, request_id: str):
        state = self._pending_requests.get(request_id)
        if state is None:
            return

        if state.retries_left > 0:
            state.retries_left -= 1
            self._execute_send_attempt(request_id=request_id)
        else:
            print(f"Client {self.node_id} FAILED {request_id}. Max retries reached. Giving up")
            del self._pending_requests[request_id]

    def _handle_client_response(self, message: Message):
        response_payload: ClientResponsePayload = message.payload
        request_id = response_payload.request_id
        if request_id in self._pending_requests:
            print(f"Client {self.node_id}: Response received for {request_id} from Node {message.src_id}, with status {response_payload.status.value}")
            del self._pending_requests[request_id]

            if response_payload.status == Status.SUCCESS:
                OracleRequest.register_new_success_request()

    def _schedule_next_loop_tick(self):
        self.send_sync(dst_id=self._node_id, msg_type=MessageType.INTERNAL_LOOP, payload=None, sync_latency=self._loop_client_period, violation_probability=0.0)

    def _schedule_next_request_timeout(self, request_id: str):
        self.send_sync(dst_id=self.node_id, msg_type=MessageType.TIMEOUT_CHECK, payload=request_id, sync_latency=self._request_timeout_period, violation_probability=0.0)