from .lowi_node import LowiNode
from .lowi_topology_strategy import LowiTopologyStrategy

from src.core.node import NodeFactory
from src.protocols.topology_factory import TopologyBuilderFactory


def register() -> None:
    NodeFactory.register(LowiNode.__name__,
        lambda node_id, network, settings: LowiNode(node_id=node_id, network=network, settings=settings)
    )
    TopologyBuilderFactory.register(name="lowi", strategy=LowiTopologyStrategy)

__all__ = [
    'LowiNode'
]

__version__ = '1.0.0'