
from dataclasses import dataclass
from typing import Any, Set, Optional


@dataclass
class PendingProposal:
    """State kept at the proposer for a single client request."""
    client_id: int
    value: Any
    proposal_number: int
    promises_from: Set[int]
    accepted_from: Set[int]
    chosen_value: Optional[Any] = None
