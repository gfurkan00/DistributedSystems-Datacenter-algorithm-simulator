from .primary_node import PrimaryNode
from .backup_node import BackupNode
from .primary_backup_topology_strategy import PrimaryBackupTopologyStrategy
from src.protocols.topology_factory import TopologyBuilderFactory

TopologyBuilderFactory.register(name="primary_backup", strategy=PrimaryBackupTopologyStrategy)

__all__ = [
    'PrimaryNode',
    'BackupNode',
]

__version__ = '1.0.0'