from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class MessageType(Enum):
    #Client
    CLIENT_REQUEST = "client_request"
    CLIENT_RESPONSE = "client_response"
    CLIENT_LOOP = "client_loop"

    #Primary Backup protocol
    REPLICATION = "replication"
    ACK = "ack"

    #Lowi
    LOOP_TICK = "loop_tick"
    TIMEOUT_CHECK = "timeout_check"
    PROPOSE = "propose"


@dataclass
class Message:
    id: str
    src_id: int
    dst_id: int
    msg_type: MessageType
    payload: Any



class Status(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

@dataclass
class ClientResponsePayload:
    request_id: str
    status: Status


@dataclass
class Event:
    delivery_time: float
    seq: int
    callback: Callable[[Message], None]
    message: Message

    def __lt__(self, other):
        return self.delivery_time < other.delivery_time