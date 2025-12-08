from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict

from src.core.utils import Message, ClientRequestPayload


@dataclass
class LowiPayload:
    cins: int
    request_id: Optional[str]
    data: Any
    is_heartbeat: bool = False

@dataclass
class LowiState:
    cins: int = 0
    lins: int = 0
    log: Dict[str, Any] = field(default_factory=dict)
    pending_requests: List[ClientRequestPayload] = field(default_factory=list)
    current_leader_id: int = 0

    def append_request(self, request: ClientRequestPayload):
        self.pending_requests.append(request)

    def pop_request(self) -> ClientRequestPayload | None:
        return self.pending_requests.pop(0) if self.pending_requests else None

    def append_decision(self, request_id: str, data: Any):
        if request_id in self.log:
            return

        self.log[request_id] = data
        self.lins = self.cins

    def get_decision(self, request_id: str) -> Optional[Any]:
        return self.log.get(request_id, None)