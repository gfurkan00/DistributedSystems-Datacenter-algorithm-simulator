from abc import ABC, abstractmethod
from typing import List

from src.config import SimulationConfig
from src.core.network import NetworkAPI
from src.core.node import Node


class TopologyServiceAPI(ABC):
    @abstractmethod
    def build_topology(self, config: SimulationConfig) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_topology(self) -> List[Node]:
        raise NotImplementedError()

    @abstractmethod
    def register_topology_into_network(self) -> None:
        raise NotImplementedError()