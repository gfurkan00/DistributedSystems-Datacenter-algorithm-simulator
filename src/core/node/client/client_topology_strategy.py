from typing import List

from src.config import SimulationConfig
from src.core.network import NetworkAPI
from src.core.node import Node
from src.core.node.client import ClientNode
from src.core.oracles import OracleRequest
from src.core.utils import NodeIDTracker
from src.protocols.topology_factory import TopologyStrategy

class NegativeWorkloadError(Exception):
    pass

class ClientTopologyStrategy(TopologyStrategy):
    def build(self, network: NetworkAPI, config: SimulationConfig) -> List[Node]:
        client_nodes: List[Node] = []
        config = config.workload_config

        if config.clients <= 0:
            raise NegativeWorkloadError("Client count must be greater than 0")

        start_id = config.start_id
        if start_id is not None:
            client_ids = NodeIDTracker.claim_range(start_id, config.clients)
        else:
            client_ids = NodeIDTracker.generate_many_random(config.clients)

        for client_id in client_ids:
            client = ClientNode(node_id=client_id, network=network, settings=config.settings)
            client_nodes.append(client)

        OracleRequest.set_total_requests(config.clients * config.settings.get("num_requests_per_client", 0))

        return client_nodes