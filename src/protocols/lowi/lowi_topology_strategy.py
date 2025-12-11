from typing import List
from src.core.node.node import Node
from src.core.network.network import NetworkAPI
from src.config import SimulationConfig
from src.core.utils import NodeIDTracker
from src.protocols.lowi import LowiNode
from src.protocols.topology_factory.topology_strategy import TopologyStrategy

class LowiTopologyStrategy(TopologyStrategy):
    def build(self, network: NetworkAPI, config: SimulationConfig) -> List[Node]:
        config = config.protocol_config
        nodes: List[Node] = []
        all_nodes_ids: List[int] = []

        for group in config.node_groups:
            if group.role_type != LowiNode.__name__:
                continue

            start_id = group.start_id
            if start_id is not None:
                ids = NodeIDTracker.claim_range(start_id, group.count)
            else:
                ids = NodeIDTracker.generate_many_random(group.count)

            all_nodes_ids.extend(ids)

        base_settings = config.settings.copy()
        base_settings["all_nodes_ids"] = all_nodes_ids

        for node_id in all_nodes_ids:
            node = LowiNode(
                node_id=node_id,
                network=network,
                settings=base_settings
            )
            nodes.append(node)

        return nodes