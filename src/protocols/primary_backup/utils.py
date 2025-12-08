from dataclasses import dataclass
from typing import Set, Any


@dataclass
class PendingRequest:
    client_id: int
    acks: Set[int]

@dataclass
class ReplicationPayload:
    request_id: str
    payload: Any