import heapq

from typing import List, Callable

from src.core.logger.logger_interface import LoggerAPI
from src.core.logger.utils import EventType
from src.core.scheduler.scheduler_interface import SchedulerAPI
from src.core.utils import Event, Message


class Scheduler(SchedulerAPI):
    def __init__(self, logger: LoggerAPI):
        self._now: float = 0.0
        self._seq: int = 0
        self._events: List[Event] = []
        self._logger: LoggerAPI = logger

    def now(self) -> float:
        return self._now

    def schedule_event(self, delay: float, callback: Callable[[Message], None], message: Message) -> None:
        self._seq += 1
        delivery_time = self._now + delay
        event = Event(delivery_time=delivery_time, seq=self._seq, callback=callback, message=message)
        heapq.heappush(self._events, event)

        self._logger.log(
            timestamp=self._now,
            source_node_id=message.src_id,
            event_type=EventType.SEND,
            dest_node_id=message.dst_id,
            request_id=message.id,
            message_type=message.msg_type,
            payload=message.payload,
        )

    def run(self, duration: int = 100) -> None:
        print("Simulation Started")

        while self._events and duration > 0:
            current_event = heapq.heappop(self._events)
            self._now = current_event.delivery_time
            current_event.callback(current_event.message)
            duration -= 1

        print("Simulation Ended")