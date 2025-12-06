from dataclasses import dataclass
from .network_config import NetworkConfig
from .protocol_config import ProtocolConfig
from .workload_config import WorkloadConfig
from typing import Optional

# Utils: Duration is how many events are going to be launched

@dataclass
class SimulationConfig:
    seed: int
    duration: int
    output_file: Optional[str]
    network_config: NetworkConfig
    protocol_config: ProtocolConfig
    workload_config: WorkloadConfig