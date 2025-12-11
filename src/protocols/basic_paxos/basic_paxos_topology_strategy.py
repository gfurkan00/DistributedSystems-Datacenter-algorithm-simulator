from typing import List, Dict, Any

from src.config import SimulationConfig
from src.core.network import NetworkAPI
from src.core.node import Node
from src.core.utils import NodeIDTracker
from src.protocols.basic_paxos import ProposerNode, AcceptorNode
from src.protocols.topology_factory import TopologyStrategy


class BasicPaxosTopologyStrategy(TopologyStrategy):
    def build(self, network: NetworkAPI, config: SimulationConfig) -> List[Node]:
        config = config.protocol_config
        nodes: List[Node] = []

        proposer_ids: List[int] = []
        acceptor_ids: List[int] = []

        for group in config.node_groups:
            if group.role_type not in (ProposerNode.__name__, AcceptorNode.__name__):
                continue

            start_id = group.start_id
            if start_id is not None:
                ids = NodeIDTracker.claim_range(start_id, group.count)
            else:
                ids = NodeIDTracker.generate_many_random(group.count)

            if group.role_type == ProposerNode.__name__:
                proposer_ids.extend(ids)
            elif group.role_type:
                acceptor_ids.extend(ids)

        for acceptor_id in acceptor_ids:
            node = AcceptorNode(node_id=acceptor_id, network=network)
            nodes.append(node)

        proposer_settings: Dict[str, Any] = {"acceptor_ids": acceptor_ids}

        for proposer_id in proposer_ids:
            node = ProposerNode(node_id=proposer_id, network=network, settings=proposer_settings)
            nodes.append(node)

        return nodes