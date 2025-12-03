from dataclasses import dataclass
from .network_config import NetworkConfig
from .node_config import NodeConfig
from .workload_config import WorkloadConfig
from typing import Optional

@dataclass
class SimulationConfig:
    seed: int

    network: NetworkConfig
    nodes: list[NodeConfig]
    workload: WorkloadConfig

    duration_seconds: Optional[float] = None
    output_file: Optional[str] = None