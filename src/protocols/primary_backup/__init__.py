from .primary_node import PrimaryNode
from .backup_node import BackupNode
from src.core.node.node_factory import NodeFactory

def register() -> None:
    NodeFactory.register("PrimaryNode", 
        lambda nid, net, cfg: PrimaryNode(nid, net, cfg.get("backup_ids", []))
    )
    NodeFactory.register("BackupNode", 
        lambda nid, net, cfg: BackupNode(nid, net)
    )

__all__ = [
    'PrimaryNode',
    'BackupNode',
]

__version__ = '1.0.0'