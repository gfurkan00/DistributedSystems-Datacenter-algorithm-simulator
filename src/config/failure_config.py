from dataclasses import dataclass
from typing import List, Union

@dataclass
class FailureEventConfig:
    time: float
    action: str
    target: Union[int, List[int]]