from .acceptor_node import AcceptorNode
from .proposer_node import ProposerNode
from .basic_paxos_topology_strategy import BasicPaxosTopologyStrategy
from ..topology_factory import TopologyBuilderFactory

def register():
    TopologyBuilderFactory.register(name="basic_paxos", strategy=BasicPaxosTopologyStrategy)

__all__ = [
    'AcceptorNode',
    'ProposerNode',
]

__version__ = '1.0.0'