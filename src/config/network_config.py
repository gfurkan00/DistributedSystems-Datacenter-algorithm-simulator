
from dataclasses import dataclass

@dataclass
class NetworkConfig:
    latency_min: float
    latency_max: float
    packet_loss_prob: float