from typing import List

from .network import NetworkAPI
from src.core.node import Node


def register_nodes_into_network(network: NetworkAPI, nodes: List[Node]) -> None:
    for node in nodes:
        network.register_node(node_id=node.node_id, receiver_callback=node.receive)