
import random
from collections.abc import Callable
from typing import Dict

from src.core.logger.logger_interface import LoggerAPI
from src.core.logger.utils import EventType
from src.core.network.network_interface import NetworkAPI
from src.core.scheduler import SchedulerAPI
from src.core.utils import Message, MessageType


class Network(NetworkAPI):
    """Simulated network with random latency and no message loss."""

    def __init__(self, scheduler: SchedulerAPI, logger: LoggerAPI, latency_min: float, latency_max: float):
        self._scheduler = scheduler
        self._logger: LoggerAPI = logger
        self._nodes: Dict[int, Callable[[Message], None]] = {}
        self._latency_min = latency_min
        self._latency_max = latency_max

    # ------------------------------------------------------------------ #
    # NetworkAPI implementation                                          #
    # ------------------------------------------------------------------ #
    def register_node(self, node_id: int, receiver_callback: Callable[[Message], None]) -> None:
        self._nodes[node_id] = receiver_callback

    def send(self, message: Message) -> None:
        """Schedule delivery of a message with random latency."""
        callback = self._nodes.get(message.dst_id)
        if callback is None:
            # Unknown destination: drop the message silently
            return

        latency = self._get_latency(message.src_id, message.dst_id)
        delivery_time = self._scheduler.now() + latency
        message.delivery_time = delivery_time

        def delivery_action(msg: Message, cb: Callable[[Message], None] = callback) -> None:
            # Log RECEIVE when the message is actually delivered
            self._logger.log(
                timestamp=self._scheduler.now(),
                source_node_id=msg.src_id,
                event_type=EventType.RECEIVE,
                dest_node_id=msg.dst_id,
                request_id=msg.id,
                message_type=msg.msg_type,
                payload=msg.payload,
            )
            cb(msg)

        # Scheduler will log SEND; we just request scheduling.
        self._scheduler.schedule_event(delay=latency, callback=delivery_action, message=message)

    # ------------------------------------------------------------------ #
    # Internal helpers                                                   #
    # ------------------------------------------------------------------ #
    def _get_latency(self, src_id: int, dst_id: int) -> float:
        # For now latency is just uniform in [min, max]
        return random.uniform(self._latency_min, self._latency_max)
