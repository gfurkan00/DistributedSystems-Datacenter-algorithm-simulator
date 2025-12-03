from abc import ABC, abstractmethod
from typing import List, Dict
from src.core.node.node import Node
from src.core.network.network import NetworkAPI
from src.config.protocol_config import ProtocolConfig

class TopologyStrategy(ABC):
    @abstractmethod
    def build(self, network: NetworkAPI, config: ProtocolConfig) -> List[Node]:
        raise NotImplementedError