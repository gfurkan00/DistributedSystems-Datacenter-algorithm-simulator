from dataclasses import dataclass
from typing import List

@dataclass
class WorkloadConfig:
    clients: List[int]
    target_id: int
    num_requests: int
