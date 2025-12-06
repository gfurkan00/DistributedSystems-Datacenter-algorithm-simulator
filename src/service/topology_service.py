from typing import List

from src.config import SimulationConfig
from src.core.network import NetworkAPI
from src.core.node import Node
from src.protocols.topology_factory import TopologyBuilderFactory
from src.service.topology_service_interface import TopologyServiceAPI

class TopologyService(TopologyServiceAPI):
    def __init__(self, network: NetworkAPI):
        self._topology: List[Node] = []
        self._network: NetworkAPI = network

    def build_topology(self, config: SimulationConfig) -> None:
        topology = []

        topology_protocol_strategy = TopologyBuilderFactory.get_strategy(config.protocol_config.name)
        created_protocol_nodes_list = topology_protocol_strategy.build(network=self._network, config=config)
        topology.extend(created_protocol_nodes_list)

        topology_client_strategy = TopologyBuilderFactory.get_strategy("client")
        created_client_nodes_list = topology_client_strategy.build(network=self._network, config=config)
        topology.extend(created_client_nodes_list)

        self._topology.extend(topology)

    def get_topology(self) -> List[Node]:
        return self._topology

    def register_topology_into_network(self) -> None:
        for node in self._topology:
            self._network.register_node(node_id=node.node_id, receiver_callback=node.receive)