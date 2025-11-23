import random

from collections.abc import Callable
from typing import Dict

from src.core.logger.logger_interface import LoggerAPI
from src.core.logger.utils import EventType
from src.core.network.network_interface import NetworkAPI
from src.core.scheduler import SchedulerAPI
from src.core.utils import Message, MessageType


class Network(NetworkAPI):
    def __init__(self, scheduler: SchedulerAPI, logger: LoggerAPI, latency_min: float, latency_max: float):
        self._scheduler = scheduler
        self._logger: LoggerAPI = logger
        self._nodes: Dict[int, Callable[[Message], None]] = {}
        self._latency_min = latency_min
        self._latency_max = latency_max

    def register_node(self, node_id: int, receiver_callback: Callable[[Message], None]):
        self._nodes[node_id] = receiver_callback

    def send(self, message: Message):
        latency = self._get_latency(message.src_id, message.dst_id)
        self._scheduler.schedule_event(delay=latency, callback=lambda msg: self._on_receive(message=msg), message=message)

    def _on_receive(self, message: Message):
        callback = self._nodes.get(message.dst_id)
        if callback is None:
            return

        self._logger.log(
            timestamp=self._scheduler.now(),
            source_node_id=message.src_id,
            event_type=EventType.RECEIVE,
            dest_node_id=message.dst_id,
            request_id=message.id,
            message_type=message.msg_type,
            payload=message.payload,
        )
        callback(message)

    def _get_latency(self, src_id: int, dst_id: int) -> float:
        return random.uniform(self._latency_min, self._latency_max)