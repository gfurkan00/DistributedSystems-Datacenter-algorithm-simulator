from typing import List
from src.core.node.node import Node
from src.core.network.network import NetworkAPI
from src.config import SimulationConfig
from src.core.utils import NodeIDTracker
from src.protocols.primary_backup import PrimaryNode, BackupNode
from src.protocols.topology_factory import TopologyStrategy

class MultiplePrimaryNodesError(Exception):
    pass

class PrimaryBackupTopologyStrategy(TopologyStrategy):
    def build(self, network: NetworkAPI, config: SimulationConfig) -> List[Node]:
        config = config.protocol_config
        nodes: List[Node] = []

        total_primaries = sum(
            group.count for group in config.node_groups
            if group.role_type == PrimaryNode.__name__
        )
        if total_primaries > 1:
            raise MultiplePrimaryNodesError("Configuration file has more than one primary node")

        primary_ids: List[int] = []
        backup_ids: List[int] = []

        for group in config.node_groups:
            if group.role_type not in (PrimaryNode.__name__, BackupNode.__name__):
                continue

            start_id = group.start_id
            if start_id is not None:
                ids = NodeIDTracker.claim_range(start_id, group.count)
            else:
                ids = NodeIDTracker.generate_many_random(group.count)

            if group.role_type == BackupNode.__name__:
                backup_ids.extend(ids)
            else:
                primary_ids.extend(ids)

        for backup_id in backup_ids:
            node = BackupNode(node_id=backup_id, network=network)
            nodes.append(node)

        primary_settings = config.settings.copy()
        primary_settings["backup_ids"] = backup_ids

        for primary_id in primary_ids:
            node = PrimaryNode(node_id=primary_id, network=network, settings=primary_settings)
            nodes.append(node)

        return nodes