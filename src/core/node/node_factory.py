from typing import Dict, Any, Callable
from src.core.node.node import Node
from src.config.node_config import NodeConfig
from src.core.network.network import NetworkAPI

NodeBuilder = Callable[[int, NetworkAPI, Dict[str, Any]], Node]

class NodeFactory:
    
    _builders: Dict[str, NodeBuilder] = {}

    @classmethod
    def register(cls, node_type: str, builder: NodeBuilder) -> None:
        cls._builders[node_type] = builder

    @classmethod
    def create(cls, config: NodeConfig, network: NetworkAPI) -> Node:
        node_type = config.type
        
        if node_type not in cls._builders:
            known_types = list(cls._builders.keys())
            raise ValueError(f"Unknown node type: '{node_type}'. Registered types: {known_types}")
            
        builder = cls._builders[node_type]
        
        extra_config = config.config if config.config else {}
        
        return builder(config.id, network, extra_config)