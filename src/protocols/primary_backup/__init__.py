from .primary_node import PrimaryNode
from .backup_node import BackupNode
from .primary_backup_topology_strategy import PrimaryBackupTopologyStrategy
from src.core.node import NodeFactory
from src.protocols.topology_factory import TopologyBuilderFactory

def register() -> None:
    NodeFactory.register(PrimaryNode.__name__,
        lambda node_id, network, settings: PrimaryNode(node_id=node_id, network=network, settings=settings)
    )
    NodeFactory.register(BackupNode.__name__,
        lambda node_id, network, settings: BackupNode(node_id=node_id, network=network)
    )
    TopologyBuilderFactory.register(name="primary_backup", strategy=PrimaryBackupTopologyStrategy)

__all__ = [
    'PrimaryNode',
    'BackupNode',
]

__version__ = '1.0.0'