from typing import Dict, Any, Callable
from src.core.node.node import Node
from src.core.network.network import NetworkAPI

NodeBuilder = Callable[[int, NetworkAPI, Dict[str, Any]], Node]

class NodeFactory:
    _BUILDERS: Dict[str, NodeBuilder] = {}

    @classmethod
    def register(cls, node_type: str, builder: NodeBuilder) -> None:
        cls._BUILDERS[node_type] = builder

    @classmethod
    def create(cls, node_type: str, node_id: int, network: NetworkAPI, protocol_settings: Dict[str, Any]) -> Node:
        if node_type not in cls._BUILDERS:
            known_types = list(cls._BUILDERS.keys())
            raise ValueError(f"Unknown node type: '{node_type}'. Registered types: {known_types}")

        builder = cls._BUILDERS[node_type]

        return builder(node_id, network, protocol_settings)