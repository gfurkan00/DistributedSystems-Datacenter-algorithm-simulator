from .lowi_node import LowiNode
from .lowi_topology_strategy import LowiTopologyStrategy

from src.protocols.topology_factory import TopologyBuilderFactory

def register():
    TopologyBuilderFactory.register(name="lowi", strategy=LowiTopologyStrategy)

__all__ = [
    'LowiNode'
]

__version__ = '1.0.0'