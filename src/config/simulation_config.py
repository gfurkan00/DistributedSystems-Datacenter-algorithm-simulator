from dataclasses import dataclass
from .network_config import NetworkConfig
from .protocol_config import ProtocolConfig
from .workload_config import WorkloadConfig
from typing import Optional

@dataclass
class SimulationConfig:
    seed: int
    duration_seconds: Optional[float]
    output_file: Optional[str]
    network_config: NetworkConfig
    protocol_config: ProtocolConfig
    workload_config: WorkloadConfig