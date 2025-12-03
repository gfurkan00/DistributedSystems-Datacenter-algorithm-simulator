from dataclasses import dataclass

@dataclass
class WorkloadConfig:
    type: str
    clients: int
    num_requests_per_client: int
