from abc import ABC, abstractmethod
from typing import List, Dict
from src.core.node.node import Node
from src.core.network.network import NetworkAPI
from src.config import SimulationConfig

class TopologyStrategy(ABC):
    @abstractmethod
    def build(self, network: NetworkAPI, config: SimulationConfig) -> List[Node]:
        raise NotImplementedError