from abc import ABC
from typing import Any, List

from .utils import EventType, LoggerEvent
from ..utils import MessageType


class LoggerAPI(ABC):
    def log(self, timestamp: float, source_node_id: int, event_type: EventType, dest_node_id: int, request_id: str, message_type: MessageType, payload: Any) -> None:
        raise NotImplementedError

    def get_logs(self) -> List[LoggerEvent]:
        raise NotImplementedError

    def print(self) -> None:
        raise NotImplementedError

    def dump_to_csv(self, filename: str) -> None:
        raise NotImplementedError