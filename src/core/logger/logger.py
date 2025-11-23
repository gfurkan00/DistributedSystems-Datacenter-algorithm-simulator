import csv

from typing import List, Any

from .logger_interface import LoggerAPI
from .utils import LoggerEvent, EventType
from ..utils import MessageType


class Logger(LoggerAPI):
    __INSTANCE: LoggerAPI = None

    def __init__(self):
        self._logs: List[LoggerEvent] = []

    @classmethod
    def create(cls) -> LoggerAPI:
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE

    def log(self, timestamp: float, source_node_id: int, event_type: EventType, dest_node_id: int, request_id: str, message_type: MessageType, payload: Any):
        logger_event = LoggerEvent(
            timestamp=timestamp,
            source_node_id=source_node_id,
            event_type=event_type,
            dest_node_id=dest_node_id,
            request_id=request_id,
            message_type=message_type,
            payload=payload
        )
        self._logs.append(logger_event)

    def print(self):
        for log in self._logs:
            print(log.to_str())

    def dump_to_csv(self, filename: str):
        if not self._logs:
            print("No logs to write")
            return
        
        try:
            with open(filename, mode='w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=LoggerEvent.fieldnames())
                writer.writeheader()
                for log in self._logs:
                    writer.writerow(log.to_dict())
            print(f"Logs successfully written to {filename}")
        except IOError as e:
            print(f"Error writing logs to CSV: {e}")