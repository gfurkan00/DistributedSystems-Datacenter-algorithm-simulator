from dataclasses import dataclass
from typing import Optional


@dataclass
class NetworkConfig:
    latency_min_wan: float
    latency_max_wan: float
    packet_loss_probability_wan: float

    latency_min_datacenter: Optional[float]
    latency_max_datacenter: Optional[float]
    packet_loss_probability_datacenter: Optional[float]