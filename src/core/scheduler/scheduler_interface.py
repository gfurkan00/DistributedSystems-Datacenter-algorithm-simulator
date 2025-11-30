from abc import abstractmethod, ABC
from typing import Callable

from src.core.utils import Message


class SchedulerAPI(ABC):
    @abstractmethod
    def now(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def schedule_event(self, delay: float, callback: Callable[[Message], None], message: Message) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self, duration: float = 100) -> None:
        raise NotImplementedError