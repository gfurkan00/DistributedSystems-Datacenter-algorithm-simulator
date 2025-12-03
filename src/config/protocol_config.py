from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class NodeGroupConfig:
    role_type: str
    count: int

@dataclass
class ProtocolConfig:
    name: str
    settings: Optional[Dict[str, Any]]
    node_groups: List[NodeGroupConfig]