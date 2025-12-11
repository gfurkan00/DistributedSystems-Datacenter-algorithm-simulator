from dataclasses import dataclass, field
from typing import Any, Set, Optional


@dataclass
class PendingProposal:
    client_id: int
    request_id: str
    value: Any
    proposal_number: int
    promises_from: Set[int] = field(default_factory=set)
    accepted_from: Set[int] = field(default_factory=set)
    highest_seen_accepted_proposal_number: int = -1
    phase2_started: bool = False
    committed: bool = False


@dataclass
class PreparePayload:
    request_id: str
    proposal_number: int

@dataclass
class PromisePayload:
    request_id: str
    proposal_number: int
    last_accepted_proposal_number: Optional[int]
    last_accepted_value: Optional[Any]

@dataclass
class AcceptPayload:
    request_id: str
    proposal_number: int
    value: Any