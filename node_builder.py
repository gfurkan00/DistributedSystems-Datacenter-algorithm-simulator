from src.config.node_config import NodeConfig
from src.core.network.network import NetworkAPI
from src.core.node.node import Node
from src.core.node.client_node import ClientNode
from src.core.node.primary_node import PrimaryNode
from src.core.node.backup_node import BackupNode
from src.core.node.paxos_node import PaxosNode


class NodeFactory:
    
    @staticmethod
    def create(node_cfg: NodeConfig, network: NetworkAPI) -> Node:
        node_type = node_cfg.type
        node_id = node_cfg.id
        config = node_cfg.config
        
        if node_type == "ClientNode":
            return ClientNode(node_id=node_id, network=network)
        elif node_type == "PrimaryNode":
            return PrimaryNode(node_id=node_id, network=network, config=config)
        elif node_type == "BackupNode":
            return BackupNode(node_id=node_id, network=network, config=config)
        elif node_type == "PaxosNode":
            return PaxosNode(node_id=node_id, network=network, config=config)
        else:
            raise ValueError(f"Unknown node type: {node_type}")
