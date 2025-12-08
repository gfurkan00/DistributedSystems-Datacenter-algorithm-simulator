
from dataclasses import dataclass, asdict, fields
from enum import Enum
from typing import Any, Dict, List

from src.core.utils import MessageType


class EventType(Enum):
    SEND = "send"
    RECEIVE = "receive"


@dataclass
class LoggerEvent:
    timestamp: float
    source_node_id: int
    event_type: EventType
    dest_node_id: int
    request_id: str
    message_type: MessageType
    payload: Any

    @classmethod
    def fieldnames(cls) -> List[str]:
        return [f.name for f in fields(cls)]

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_str(self) -> str:
        return (
            f"[Time {self.timestamp}] "
            f"Source Node Id {self.source_node_id} "
            f"Event {self.event_type.value} "
            f"Destination Node Id {self.dest_node_id} "
            f"Request Id {self.request_id} "
            f"Message type {self.message_type.name} "
            f"Payload {self.payload}"
        )
