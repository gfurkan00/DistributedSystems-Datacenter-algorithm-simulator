from typing import Dict, Any, Type
from src.core.node.node import Node
from src.core.node.client_node import ClientNode
from src.protocols.primary_backup.primary_node import PrimaryNode
from src.protocols.primary_backup.backup_node import BackupNode
from src.config.node_config import NodeConfig
from src.core.network.network import NetworkAPI

class NodeFactory:
    """Factory to create nodes based on configuration."""
    
    @staticmethod
    def create(config: NodeConfig, network: NetworkAPI) -> Node:
        node_type = config.type
        node_id = config.id
        
        if node_type == "ClientNode":
            return ClientNode(node_id, network)
            
        elif node_type == "PrimaryNode":
            backup_ids = []
            if config.config and "backup_ids" in config.config:
                backup_ids = config.config["backup_ids"]
            
            return PrimaryNode(node_id, network, backup_ids)
            
        elif node_type == "BackupNode":
            return BackupNode(node_id, network)
            
        else:
            raise ValueError(f"Unknown node type: {node_type}")