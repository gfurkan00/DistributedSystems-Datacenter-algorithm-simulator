from typing import Any

from .utils import Message, MessageType
from .uuid import new_uuid


class MessageFactory:
    @staticmethod
    def build_message(src_id: int, dst_id: int, msg_type: MessageType, payload: Any) -> Message:
        return Message(id=new_uuid(), src_id=src_id, dst_id=dst_id, msg_type=msg_type, payload=payload)

    @staticmethod
    def print_message(message: Message) -> None:
        print(f"Message: id {message.id}, source id: {message.src_id}, destination id: {message.dst_id}, msg_type: {message.msg_type}, payload: {message.payload}")