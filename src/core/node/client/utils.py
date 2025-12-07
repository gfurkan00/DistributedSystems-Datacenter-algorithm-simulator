from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class PendingRequestState:
    request_id: str
    payload_data: Any
    retries_left: int