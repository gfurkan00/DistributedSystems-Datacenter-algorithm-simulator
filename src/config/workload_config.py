from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class WorkloadConfig:
    type: str
    start_id: Optional[int]
    clients: int
    settings: Optional[Dict[str, Any]]
