from typing import List
from src.core.node.node_factory import NodeFactory
from src.core.node.node import Node
from src.core.network.network import NetworkAPI
from src.config.protocol_config import ProtocolConfig
from src.core.utils import NodeIDGenerator
from src.protocols.primary_backup import PrimaryNode, BackupNode
from src.protocols.topology_factory import TopologyStrategy


class PrimaryBackupTopologyStrategy(TopologyStrategy):
    def build(self, network: NetworkAPI, config: ProtocolConfig) -> List[Node]:
        nodes: List[Node] = []

        total_primaries = sum(group.count for group in config.node_groups if group.role_type == PrimaryNode.__name__)
        total_backups = sum(group.count for group in config.node_groups if group.role_type == BackupNode.__name__)

        needed_ids = NodeIDGenerator.generate_many(total_primaries + total_backups)

        primary_ids = needed_ids[:total_primaries]
        backup_ids = needed_ids[total_primaries:]

        backup_settings = config.settings.copy()
        for backup_id in backup_ids:
            node = NodeFactory.create(BackupNode.__name__, backup_id, network, backup_settings)
            nodes.append(node)

        primary_settings = config.settings.copy()
        primary_settings["backup_ids"] = backup_ids

        for primary_id in primary_ids:
            node = NodeFactory.create(PrimaryNode.__name__, primary_id, network, primary_settings)
            nodes.append(node)

        return nodes