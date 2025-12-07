from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class MessageType(Enum):
    #Client
    CLIENT_REQUEST = "client_request"
    CLIENT_RESPONSE = "client_response"

    #Primary Backup protocol
    REPLICATION = "replication"
    ACK = "ack"

    #Lowi
    PROPOSE = "propose"

    #General
    INTERNAL_LOOP = "internal_loop"
    TIMEOUT_CHECK = "timeout_check"


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
class ClientRequestPayload:
    request_id: str
    data: Any

@dataclass
class Event:
    delivery_time: float
    seq: int
    callback: Callable[[Message], None]
    message: Message

    def __lt__(self, other):
        return self.delivery_time < other.delivery_time