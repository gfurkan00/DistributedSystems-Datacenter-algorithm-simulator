import csv

from typing import List, Any, Optional

from .logger_interface import LoggerAPI
from .utils import LoggerEvent, EventType
from ..utils import MessageType


class Logger(LoggerAPI):
    def __init__(self):
        self._logs: List[LoggerEvent] = []

    def log(self, timestamp: float, source_node_id: int, event_type: EventType, dest_node_id: Optional[int], message_id: Optional[str], message_type: Optional[MessageType], payload: Optional[Any]):
        if message_type == MessageType.INTERNAL_LOOP or message_type == MessageType.TIMEOUT_CHECK:
            return

        logger_event = LoggerEvent(
            timestamp=timestamp,
            source_node_id=source_node_id,
            event_type=event_type,
            dest_node_id=dest_node_id,
            message_id=message_id,
            message_type=message_type,
            payload=payload
        )
        self._logs.append(logger_event)

    def get_logs(self) -> List[LoggerEvent]:
        return self._logs

    def print(self):
        for logger_event in self._logs:
            print(logger_event.to_str())

    def dump_to_csv(self, filename: str):
        if not self._logs:
            print("No logs to write")
            return
        
        try:
            with open(filename, mode='w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=LoggerEvent.fieldnames())
                writer.writeheader()
                for logger_event in self._logs:
                    writer.writerow(logger_event.to_dict())
            print(f"Logs successfully written to {filename}")
        except IOError as e:
            print(f"Error writing logs to CSV: {e}")