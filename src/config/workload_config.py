from dataclasses import dataclass
from typing import Optional,List

@dataclass
class RequestConfig:
    payload: str
    delay: float



@dataclass
class WorkloadConfig:
    type: str
    client_id: int
    target_id: int
    requests: Optional[list[RequestConfig]] = None
    num_requests: Optional[int] = None
