from src.core.node import Node
from src.core.utils import Message, MessageType

class MultiPaxosAcceptor(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.promised_term = -1
        self.accepted = {}
        self.alive = True

    def receive(self, msg: Message):
        if not self.alive:
            return

        payload = msg.payload

        if msg.msg_type == MessageType.LEADER_PREPARE:
            term = payload['term']
            if term > self.promised_term:
                self.promised_term = term
                reply = Message(
                    id=f"promise-{msg.id}",
                    src_id=self.id,
                    dst_id=msg.src_id,
                    msg_type=MessageType.LEADER_PROMISE,
                    payload={
                        "term": term,
                        "accepted": self.accepted
                    },
                    delivery_time=self._scheduler.now()
                )
                self._send(reply)

        elif msg.msg_type == MessageType.FAST_ACCEPT:
            term = payload['term']
            index = payload['index']
            value = payload['value']
            if term >= self.promised_term:
                self.promised_term = term
                self.accepted[index] = (term, value)
                reply = Message(
                    id=f"accepted-{msg.id}",
                    src_id=self.id,
                    dst_id=msg.src_id,
                    msg_type=MessageType.FAST_ACCEPTED,
                    payload={
                        "term": term,
                        "index": index
                    },
                    delivery_time=self._scheduler.now()
                )
                self._send(reply)
