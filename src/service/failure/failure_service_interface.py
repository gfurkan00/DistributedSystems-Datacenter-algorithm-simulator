from abc import ABC
from typing import List

from src.config import FailureEventConfig


class FailureServiceAPI(ABC):
    def schedule_failures(self, failure_configs: List[FailureEventConfig]):
        raise NotImplementedError()