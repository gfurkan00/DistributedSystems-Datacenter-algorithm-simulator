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
        data = asdict(self)
        # Clean up Enums for CSV
        if isinstance(self.event_type, Enum):
            data['event_type'] = self.event_type.value
        if isinstance(self.message_type, Enum):
            data['message_type'] = self.message_type.name
        # Format timestamp
        data['timestamp'] = f"{self.timestamp:.4f}"
        return data

    def to_str(self) -> str:
        evt = self.event_type.value if isinstance(self.event_type, Enum) else self.event_type
        msg_type = self.message_type.name if isinstance(self.message_type, Enum) else self.message_type
        return f"[{self.timestamp:.4f}] Node {self.source_node_id} -> Node {self.dest_node_id} | {evt.upper()} | {msg_type} | Req: {self.request_id} | Payload: {self.payload}"