import heapq

from typing import List, Callable

from src.core.scheduler.scheduler_interface import SchedulerAPI
from src.core.utils import Event


class Scheduler(SchedulerAPI):
    def __init__(self):
        self._now: float = 0.0
        self._seq: int = 0
        self._events: List[Event] = []

    def now(self) -> float:
        return self._now

    def schedule_event(self, delay: float, callback: Callable[[], None]) -> None:
        self._seq += 1
        delivery_time = self._now + delay
        event = Event(delivery_time=delivery_time, seq=self._seq, callback=callback)
        heapq.heappush(self._events, event)

    def run(self, duration: int) -> None:
        print("Simulation Started")

        while self._events and duration > 0:
            current_event = heapq.heappop(self._events)
            self._now = current_event.delivery_time
            current_event.callback()
            duration -= 1

        print("Simulation Ended")