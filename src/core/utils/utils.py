
from dataclasses import dataclass
from enum import Enum
from typing import Any


class MessageType(Enum):
    CLIENT_REQUEST = "CLIENT_REQUEST"
    CLIENT_RESPONSE = "CLIENT_RESPONSE"
    REPLICATION = "REPLICATION"
    ACK = "ACK"
    PREPARE = "PREPARE"
    PROMISE = "PROMISE"
    ACCEPT = "ACCEPT"
    ACCEPTED = "ACCEPTED"


@dataclass
class Message:
    """Represents a message travelling in the simulated network."""
    id: str
    src_id: int
    dst_id: int
    msg_type: MessageType
    payload: Any
    # Absolute delivery time in the simulated timeline
    delivery_time: float

    def __lt__(self, other: "Message") -> bool:
        # Needed so messages / events can be ordered in heaps
        return self.delivery_time < other.delivery_time


@dataclass
class Event:
    """Generic event container (not heavily used in this project).

    The scheduler defines its own internal event structure; this
    class is kept only for compatibility with existing imports.
    """
    delivery_time: float
    seq: int
    callback: Any
    message: Message
