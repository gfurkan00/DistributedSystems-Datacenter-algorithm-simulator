from dataclasses import dataclass
from typing import Optional


@dataclass
class WorkloadConfig:
    type: str
    start_id: Optional[int]
    clients: int
    num_requests_per_client: int
