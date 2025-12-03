from typing import List
from src.core.node.node import Node
from src.core.network.network import NetworkAPI
from src.config.protocol_config import ProtocolConfig
from src.core.utils import NodeIDGenerator
from src.protocols.lowi import LowiNode
from src.protocols.topology_factory.topology_strategy import TopologyStrategy

class LowiTopologyStrategy(TopologyStrategy):
    def build(self, network: NetworkAPI, config: ProtocolConfig) -> List[Node]:
        nodes: List[Node] = []

        total_nodes_count = sum(group.count for group in config.node_groups if group.role_type == LowiNode.__name__)

        all_nodes_ids = NodeIDGenerator.generate_many(total_nodes_count)

        base_settings = config.settings.copy()
        base_settings["all_nodes_ids"] = all_nodes_ids

        current_idx = 0
        for group in config.node_groups:
            for _ in range(group.count):
                node_id = all_nodes_ids[current_idx]

                node = LowiNode(
                    node_id=node_id,
                    network=network,
                    settings=base_settings
                )
                nodes.append(node)
                current_idx += 1

        return nodes