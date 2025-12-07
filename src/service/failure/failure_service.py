from typing import List

from .failure_service_interface import FailureServiceAPI
from src.core.scheduler import SchedulerAPI
from src.service.topology import TopologyServiceAPI
from src.config import FailureEventConfig


class FailureService(FailureServiceAPI):
    def __init__(self, scheduler: SchedulerAPI, topology_service: TopologyServiceAPI):
        self._scheduler = scheduler
        self._topology_service = topology_service

    def schedule_failures(self, failure_configs: List[FailureEventConfig]):
        if not failure_configs:
            return

        for event in failure_configs:
            targets = event.target if isinstance(event.target, list) else [event.target]

            def make_callback(action, target_list):
                return lambda: self._execute_failure(action=action, target_ids=target_list)

            self._scheduler.schedule_event(
                delay=event.time,
                callback=make_callback(event.action, targets)
            )

    def _execute_failure(self, action: str, target_ids: List[int]):
        for node_id in target_ids:
            if action == "crash":
                self._topology_service.node_crash(node_id=node_id)