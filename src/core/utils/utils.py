from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class MessageType(Enum):
    CLIENT_REQUEST = "client_request"
    CLIENT_RESPONSE = "client_response"
    REPLICATION = "replication"
    ACK = "ack"


@dataclass
class Message:
    id: str
    src_id: int
    dst_id: int
    msg_type: MessageType
    payload: Any


@dataclass
class Event:
    delivery_time: float
    seq: int
    callback: Callable[[Message], None]
    message: Message

    def __lt__(self, other):
        return self.delivery_time < other.delivery_time