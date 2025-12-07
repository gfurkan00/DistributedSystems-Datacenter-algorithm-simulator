from abc import ABC, abstractmethod
from typing import List, Optional

from src.config import SimulationConfig
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

    @abstractmethod
    def node_crash(self, node_id: int) -> None:
        raise NotImplementedError()