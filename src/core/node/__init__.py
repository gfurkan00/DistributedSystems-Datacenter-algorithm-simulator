from .node import Node
from .client_node import ClientNode
from .node_factory import NodeFactory


__all__ = [
    'Node',
    'ClientNode',
]

def register() -> None:
    NodeFactory.register("ClientNode", lambda nid, net, cfg: ClientNode(nid, net))

__version__ = '1.0.0'