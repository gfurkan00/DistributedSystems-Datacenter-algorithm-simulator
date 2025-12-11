import random

from collections.abc import Callable
from typing import Dict

from src.config import NetworkConfig
from src.core.logger.logger_interface import LoggerAPI
from src.core.logger.utils import EventType
from src.core.network.network_interface import NetworkAPI
from src.core.scheduler import SchedulerAPI
from src.core.utils import Message, MessageType


class Network(NetworkAPI):
    def __init__(self, scheduler: SchedulerAPI, logger: LoggerAPI, network_config: NetworkConfig):
        self._scheduler = scheduler
        self._logger: LoggerAPI = logger
        self._nodes: Dict[int, Callable[[Message], None]] = {}
        self._latency_min_wan = network_config.latency_min_wan
        self._latency_max_wan = network_config.latency_max_wan
        self._packet_loss_probability_wan = network_config.packet_loss_probability_wan

        self._latency_min_datacenter = network_config.latency_min_datacenter
        self._latency_max_datacenter = network_config.latency_max_datacenter
        self._packet_loss_probability_datacenter = network_config.packet_loss_probability_datacenter

    def now(self) -> float:
        return self._scheduler.now()

    def register_node(self, node_id: int, receiver_callback: Callable[[Message], None]):
        self._nodes[node_id] = receiver_callback

    def remove_node(self, node_id: int):
        if node_id not in self._nodes:
            raise KeyError(f"Node {node_id} does not exist")

        del self._nodes[node_id]
        self._logger.log(
            timestamp=self._scheduler.now(),
            source_node_id=node_id,
            event_type=EventType.DIE,
            dest_node_id=None,
            message_id=None,
            message_type=None,
            payload=None,
        )

    def send(self, message: Message):
        if self._is_packet_loss(message_type=message.msg_type):
            self._logger.log(
                timestamp=self._scheduler.now(),
                source_node_id=message.src_id,
                event_type=EventType.DROP,
                dest_node_id=message.dst_id,
                message_id=message.id,
                message_type=message.msg_type,
                payload=message.payload,
            )
            return

        self._logger.log(
            timestamp=self._scheduler.now(),
            source_node_id=message.src_id,
            event_type=EventType.SEND,
            dest_node_id=message.dst_id,
            message_id=message.id,
            message_type=message.msg_type,
            payload=message.payload,
        )

        latency = self._get_latency(message_type=message.msg_type)
        self._scheduler.schedule_event(delay=latency, callback=lambda: self._on_receive(message))

    def send_sync(self, message: Message, sync_latency: float, violation_probability: float):
        if random.random() < violation_probability:
            self._logger.log(
                timestamp=self._scheduler.now(),
                source_node_id=message.src_id,
                event_type=EventType.DROP,
                dest_node_id=message.dst_id,
                message_id=message.id,
                message_type=message.msg_type,
                payload=message.payload,
            )
            return

        self._logger.log(
            timestamp=self._scheduler.now(),
            source_node_id=message.src_id,
            event_type=EventType.SEND,
            dest_node_id=message.dst_id,
            message_id=message.id,
            message_type=message.msg_type,
            payload=message.payload,
        )
        self._scheduler.schedule_event(delay=sync_latency, callback=lambda: self._on_receive(message))

    def _on_receive(self, message: Message):
        callback = self._nodes.get(message.dst_id)
        if callback is None:
            return

        self._logger.log(
            timestamp=self._scheduler.now(),
            source_node_id=message.src_id,
            event_type=EventType.RECEIVE,
            dest_node_id=message.dst_id,
            message_id=message.id,
            message_type=message.msg_type,
            payload=message.payload,
        )
        callback(message)

    def _get_latency(self, message_type: MessageType) -> float:
        if message_type == MessageType.CLIENT_REQUEST or message_type == MessageType.CLIENT_RESPONSE:
            return random.uniform(self._latency_min_wan, self._latency_max_wan)
        else:
            return random.uniform(self._latency_min_datacenter, self._latency_max_datacenter)

    def _is_packet_loss(self, message_type: MessageType)-> bool:
        if message_type == MessageType.CLIENT_REQUEST or message_type == MessageType.CLIENT_RESPONSE:
            return random.random() < self._packet_loss_probability_wan
        else:
            return random.random() < self._packet_loss_probability_datacenter