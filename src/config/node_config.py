from dataclasses import dataclass
from typing import Optional,Dict,Any

@dataclass
class NodeConfig:
    id: int
    type: str
    protocol: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    