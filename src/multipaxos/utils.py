from dataclasses import dataclass
from typing import Any

@dataclass
class LogEntry:
    index: int
    value: Any
    term: int

@dataclass
class PendingFastAccept:
    index: int
    term: int
    value: Any
    accepted_from: set
