from src.protocols.topology_factory import TopologyBuilderFactory
from .client_node import ClientNode
from .client_topology_strategy import ClientTopologyStrategy

def register():
    TopologyBuilderFactory.register(name="client", strategy=ClientTopologyStrategy)

__all__ = [
    'ClientNode',
    'ClientTopologyStrategy',
]

__version__ = '1.0.0'