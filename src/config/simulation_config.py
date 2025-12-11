from dataclasses import dataclass, field

from .failure_config import FailureEventConfig
from .network_config import NetworkConfig
from .protocol_config import ProtocolConfig
from .workload_config import WorkloadConfig
from typing import Optional, List


# Utils: Duration is how many events are going to be launched

@dataclass
class SimulationConfig:
    seed: Optional[int]
    duration: int
    output_file: Optional[str]
    network_config: NetworkConfig
    protocol_config: ProtocolConfig
    workload_config: WorkloadConfig
    failures: List[FailureEventConfig] = field(default_factory=list)