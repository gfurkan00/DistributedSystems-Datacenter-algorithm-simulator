
from abc import ABC, abstractmethod
from typing import Any

from .utils import EventType
from ..utils import MessageType


class LoggerAPI(ABC):
    @abstractmethod
    def log(
        self,
        timestamp: float,
        source_node_id: int,
        event_type: EventType,
        dest_node_id: int,
        request_id: str,
        message_type: MessageType,
        payload: Any,
    ) -> None:
        """Record a new logging event."""
        raise NotImplementedError

    @abstractmethod
    def print(self) -> None:
        """Print all logs to stdout in a human‑readable way."""
        raise NotImplementedError

    @abstractmethod
    def dump_to_csv(self, filename: str) -> None:
        """Persist logs to a CSV file."""
        raise NotImplementedError
