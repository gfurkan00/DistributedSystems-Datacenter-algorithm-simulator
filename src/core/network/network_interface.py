from abc import ABC, abstractmethod
from typing import Callable

from src.core.utils import Message


class NetworkAPI(ABC):
    @abstractmethod
    def now(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def register_node(self, node_id: int, receiver_callback: Callable[[Message], None]):
        raise NotImplementedError

    @abstractmethod
    def send(self, message: Message) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_sync(self, message: Message, sync_latency: float = 0.5) -> None:
        raise NotImplementedError