from typing import Dict, Any

from src.core.network import NetworkAPI
from src.core.node import Node
from src.core.utils import MessageType, Message, ClientResponsePayload, Status, Oracle, ClientRequestPayload
from src.protocols.lowi.utils import LowiState, LowiPayload


class LowiNode(Node):
    def __init__(self, node_id: int, network: NetworkAPI, settings: Dict[str, Any]):
        super().__init__(node_id, network)
        self._all_nodes = sorted(settings.get("all_nodes_ids", []))
        if not self._all_nodes:
            raise ValueError("All nodes ids must be specified")

        self._state = LowiState(current_leader_id=self._all_nodes[0])

        #Dictionary with request_id as key and client_id who sent request as value
        self._pending_client_requests: Dict[str, int] = {}

        self._loop_leader_period = settings.get("loop_leader_period", 0.2)
        self._timeout_follower_period = settings.get("timeout_follower_period", 0.5)

        self._timeout_limit = settings.get("timeout_limit", 2.5)
        self._sync_latency = settings.get("sync_latency", 0.1)

        self._violation_synchronous_probability = settings.get("violation_synchronous_probability", 0.01)

        self._last_leader_contact_follower_time = 0.0

        self._schedule_next_timeout_check()
        if self.is_leader:
            Oracle.set_leader_id(self._node_id)
            self._schedule_next_loop_tick()

    @property
    def is_leader(self):
        return self._node_id == self._state.current_leader_id

    def receive(self, msg: Message):
        if not self.is_alive:
            return

        current_time = self._network.now()

        if msg.msg_type == MessageType.CLIENT_REQUEST:
            self._handle_client_request(msg)

        elif msg.msg_type == MessageType.PROPOSE:
            self._handle_proposal(msg, current_time)

        elif msg.msg_type == MessageType.INTERNAL_LOOP:
            self._run_leader_loop()

        elif msg.msg_type == MessageType.TIMEOUT_CHECK:
            self._check_leader_health(current_time)

    def _handle_client_request(self, msg: Message):
        if self.is_leader:
            client_payload: ClientRequestPayload = msg.payload
            self._pending_client_requests[client_payload.request_id] = msg.src_id
            self._state.append_request(client_payload)
            print(f"Node {self._node_id} save CLIENT REQUEST {client_payload.request_id}")

    def _run_leader_loop(self):
        if not self.is_leader:
            return

        if self._state.cins == self._state.lins:
            self._state.cins += 1
            payload = self._create_proposal_payload()
            self._broadcast_proposal(payload)

            if not payload.is_heartbeat:
                self._state.append_decision(payload.data)
                self._send_client_response(payload.request_id, Status.SUCCESS)
            else:
                self._state.cins = self._state.lins

        self._schedule_next_loop_tick()

    def _create_proposal_payload(self) -> LowiPayload:
        request = self._state.pop_request()
        if request:
            return LowiPayload(
                cins=self._state.cins,
                request_id=request.request_id,
                data=request.data,
                is_heartbeat=False
            )
        else:
            return LowiPayload(
                cins=self._state.cins,
                request_id=None,
                data=None,
                is_heartbeat=True
            )

    def _broadcast_proposal(self, payload: LowiPayload):
        for dst_id in self._all_nodes:
            if dst_id != self._node_id:
                print(f"Node {self._node_id} send PROPOSE {payload.data} to {dst_id}. Is heartbeat? {payload.is_heartbeat}")
                self.send_sync(dst_id=dst_id, msg_type=MessageType.PROPOSE, payload=payload, sync_latency=self._sync_latency, violation_probability=self._violation_synchronous_probability)


    def _send_client_response(self, request_id: str, status: Status):
        client_id = self._pending_client_requests[request_id]
        client_response_payload: ClientResponsePayload = ClientResponsePayload(request_id=request_id, status=status)
        self.send(dst_id=client_id, msg_type=MessageType.CLIENT_RESPONSE, payload=client_response_payload)
        del self._pending_client_requests[request_id]

    def _handle_proposal(self, msg: Message, now: float):
        sender = msg.src_id
        payload: LowiPayload = msg.payload

        print(f"Node {self._node_id} receive PROPOSE from {msg.src_id}. Is heartbeat? {payload.is_heartbeat}")

        if sender > self._state.current_leader_id:
            self._switch_leader(sender, now)

        if sender == self._state.current_leader_id:
            self._last_leader_contact_follower_time = now

            if payload.is_heartbeat:
                self._state.cins = self._state.lins
            else:
                self._state.append_decision(payload.data)
                self._state.cins = payload.cins
                self._state.lins = payload.cins
                print(f"Node {self._node_id} COMMITTED: {payload.data}")


    def _check_leader_health(self, now: float):
        if not self.is_leader:
            if now - self._last_leader_contact_follower_time > self._timeout_limit:
                print(f"Node {self._node_id} notice Leader TIMEOUT: Leader {self._state.current_leader_id} is dead")
                self._perform_deterministic_election(now)

        self._schedule_next_timeout_check()

    def _perform_deterministic_election(self, now: float):
        current_leader_index = self._all_nodes.index(self._state.current_leader_id)
        next_leader_idx = (current_leader_index + 1) % len(self._all_nodes)
        new_leader_id = self._all_nodes[next_leader_idx]

        self._switch_leader(new_leader_id, now)

        if self.is_leader:
            print(f"Node {self._node_id} became leader")
            Oracle.set_leader_id(self._node_id)
            self._schedule_next_loop_tick()

    def _switch_leader(self, new_leader_id: int, now: float):
        self._state.current_leader_id = new_leader_id
        self._last_leader_contact_follower_time = now

    def _schedule_next_loop_tick(self):
        if not self.is_leader:
            return
        self.send_sync(dst_id=self._node_id, msg_type=MessageType.INTERNAL_LOOP, payload=None, sync_latency=self._loop_leader_period, violation_probability=0.0)

    def _schedule_next_timeout_check(self):
        self.send_sync(dst_id=self._node_id, msg_type=MessageType.TIMEOUT_CHECK, payload=None, sync_latency=self._timeout_follower_period, violation_probability=0.0)