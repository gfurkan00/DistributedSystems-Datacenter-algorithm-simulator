from dataclasses import dataclass, asdict, fields
from enum import Enum
from typing import Any, Dict, List

from src.core.utils import MessageType


class EventType(Enum):
    SEND = "send"
    RECEIVE = "receive"
    DROP = "drop"


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
        data['event_type'] = self.event_type.name
        data['message_type'] = self.message_type.name
        data['timestamp'] = f"{self.timestamp:.4f}"
        return data

    def to_str(self) -> str:
        event_type = self.event_type.name
        msg_type = self.message_type.name
        return f"[{self.timestamp:.4f}] Node {self.source_node_id} -> Node {self.dest_node_id} | {event_type.upper()} | {msg_type.upper()} | Req: {self.request_id} | Payload: {self.payload}"