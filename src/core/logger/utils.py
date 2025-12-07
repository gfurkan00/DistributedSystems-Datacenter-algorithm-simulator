from dataclasses import dataclass, asdict, fields
from enum import Enum
from typing import Any, Dict, List, Optional

from src.core.utils import MessageType


class EventType(Enum):
    SEND = "send"
    RECEIVE = "receive"
    DROP = "drop"
    DIE = "die"


@dataclass
class LoggerEvent:
    timestamp: float
    source_node_id: int
    event_type: EventType
    dest_node_id: Optional[int]
    message_id: Optional[str]
    message_type: Optional[MessageType]
    payload: Optional[Any]

    @classmethod
    def fieldnames(cls) -> List[str]:
        return [f.name for f in fields(cls)]

    def to_dict(self) -> Dict:
        data = asdict(self)
        data['event_type'] = self.event_type.name
        data['message_type'] = self.message_type.name if self.message_type is not None else ''
        data['timestamp'] = f"{self.timestamp:.4f}"
        return data

    def to_str(self) -> str:
        event_type = self.event_type.name
        msg_type = self.message_type.name if self.message_type is not None else ''
        return f"[{self.timestamp:.4f}] Node {self.source_node_id} -> Node {self.dest_node_id} | {event_type.upper()} | {msg_type.upper()} | Message ID: {self.message_id} | Payload: {self.payload}"