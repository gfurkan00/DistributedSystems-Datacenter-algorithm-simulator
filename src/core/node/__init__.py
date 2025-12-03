from .node import Node
from .client_node import ClientNode
from .node_factory import NodeFactory


__all__ = [
    'Node',
    'ClientNode',
    'NodeFactory'
]

def register() -> None:
    NodeFactory.register("ClientNode", lambda node_id, network, settings: ClientNode(node_id=node_id, network=network))

__version__ = '1.0.0'