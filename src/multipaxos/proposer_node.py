from src.core.node import Node
from src.core.utils import Message, MessageType
from src.protocols.multipaxos.utils import PendingFastAccept
from src.protocols.multipaxos.leader_state import LeaderState

class MultiPaxosProposer(Node):
    def __init__(self, *args, acceptor_ids=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.acceptor_ids = acceptor_ids or []
        self.leader = LeaderState()
        self.log = {}
        self.commit_index = -1
        self.pending_fast = {}
        self.promises = set()

    def handle_client(self, msg):
        if not self.leader.phase1_done:
            self.start_leader_election()
            return

        index = self.commit_index + 1
        term = self.leader.current_term
        value = msg.payload['value']

        self.pending_fast[index] = PendingFastAccept(
            index=index,
            term=term,
            value=value,
            accepted_from=set()
        )

        for aid in self.acceptor_ids:
            m = Message(
                id=f"fastaccept-{index}-{aid}",
                src_id=self.id,
                dst_id=aid,
                msg_type=MessageType.FAST_ACCEPT,
                payload={
                    "term": term,
                    "index": index,
                    "value": value,
                },
                delivery_time=self._scheduler.now()
            )
            self._send(m)

    def start_leader_election(self):
        self.leader.start_new_term(self.id)
        self.promises.clear()

        for aid in self.acceptor_ids:
            m = Message(
                id=f"prepare-{aid}",
                src_id=self.id,
                dst_id=aid,
                msg_type=MessageType.LEADER_PREPARE,
                payload={"term": self.leader.current_term},
                delivery_time=self._scheduler.now()
            )
            self._send(m)

    def receive(self, msg):
        payload = msg.payload

        if msg.msg_type == MessageType.CLIENT_REQUEST:
            self.handle_client(msg)

        elif msg.msg_type == MessageType.LEADER_PROMISE:
            if payload['term'] == self.leader.current_term:
                self.promises.add(msg.src_id)
                majority = len(self.acceptor_ids) // 2 + 1
                if len(self.promises) >= majority:
                    self.leader.become_leader()

        elif msg.msg_type == MessageType.FAST_ACCEPTED:
            index = payload['index']
            if index not in self.pending_fast:
                return

            state = self.pending_fast[index]
            state.accepted_from.add(msg.src_id)
            majority = len(self.acceptor_ids) // 2 + 1

            if len(state.accepted_from) >= majority:
                self.log[index] = state.value
                self.commit_index = index
                client_reply = Message(
                    id=f"commit-{index}",
                    src_id=self.id,
                    dst_id=99,
                    msg_type=MessageType.CLIENT_RESPONSE,
                    payload={
                        "status": "committed",
                        "value": state.value
                    },
                    delivery_time=self._scheduler.now()
                )
                self._send(client_reply)
