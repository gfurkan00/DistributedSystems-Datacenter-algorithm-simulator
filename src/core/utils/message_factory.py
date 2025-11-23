import uuid

from typing import Any

from src.core.utils import Message, MessageType


class MessageFactory:
    @staticmethod
    def build_message(src_id: int, dst_id: int, msg_type: MessageType, payload: Any) -> Message:
        return Message(id=str(uuid.uuid4()), src_id=src_id, dst_id=dst_id, msg_type=msg_type, payload=payload)

    @staticmethod
    def print_message(message: Message) -> None:
        print(f"Message: id {message.id}, source id: {message.src_id}, destination id: {message.dst_id}, msg_type: {message.msg_type}, payload: {message.payload}")