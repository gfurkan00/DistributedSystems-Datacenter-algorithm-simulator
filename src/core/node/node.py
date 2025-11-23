import random

from abc import ABC, abstractmethod
from typing import Any

from src.core.network import NetworkAPI
from src.core.utils import Message, MessageType, MessageFactory


class Node(ABC):
    def __init__(self, node_id: int, network: NetworkAPI):
        self._node_id: int = node_id
        self._network: NetworkAPI = network

    @property
    def node_id(self) -> int:
        return self._node_id

    def send(self, dst_id: int, msg_type: MessageType, payload: Any):
        message = MessageFactory.build_message(src_id=self._node_id, dst_id=dst_id, msg_type=msg_type, payload=payload)
        self._network.send(message=message)

    @abstractmethod
    def receive(self, msg: Message):
        raise NotImplementedError