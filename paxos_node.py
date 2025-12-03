from typing import Dict, Any, Optional, Set
from src.core.node.node import Node
from src.core.network.network import NetworkAPI
from src.core.utils.utils import MessageType, Message


class PaxosNode(Node):
    
    def __init__(self, node_id: int, network: NetworkAPI, config: Optional[Dict[str, Any]] = None):
        super().__init__(node_id, network)
        
        if config:
            self.proposer_ids = set(config.get("proposer_ids", []))
            self.acceptor_ids = set(config.get("acceptor_ids", []))
            self.learner_ids = set(config.get("learner_ids", []))
        else:
            self.proposer_ids = set()
            self.acceptor_ids = set()
            self.learner_ids = set()
        
        self.is_proposer = node_id in self.proposer_ids
        self.is_acceptor = node_id in self.acceptor_ids
        self.is_learner = node_id in self.learner_ids
        
        self.proposal_number = node_id
        self.current_value = None
        self.promises = {}
        self.promise_values = {}
        
        self.highest_promised = {}
        self.accepted = {}
        
        self.accepted_msgs = {}
        self.learned = {}
        
        self.client_requests = {}
    
    def get_next_proposal_num(self):
        self.proposal_number += len(self.proposer_ids)
        return self.proposal_number
    
    def get_quorum(self):
        return len(self.acceptor_ids) // 2 + 1
    
    def handle_client_request(self, msg: Message):
        if not self.is_proposer:
            return
        
        req_id = msg.request_id
        self.current_value = msg.payload
        self.client_requests[req_id] = msg.source_node_id
        
        self.promises[req_id] = set()
        self.promise_values[req_id] = {}
        
        n = self.get_next_proposal_num()
        for acceptor_id in self.acceptor_ids:
            self.send(
                dst_id=acceptor_id,
                msg_type=MessageType.PAXOS_PREPARE,
                payload={"n": n},
                request_id=req_id
            )
    
    def handle_promise(self, msg: Message):
        req_id = msg.request_id
        acceptor_id = msg.source_node_id
        payload = msg.payload
        
        if req_id not in self.promises:
            return
        
        self.promises[req_id].add(acceptor_id)
        
        if "accepted_n" in payload and payload["accepted_n"] is not None:
            self.promise_values[req_id][acceptor_id] = (payload["accepted_n"], payload["accepted_value"])
        
        if len(self.promises[req_id]) >= self.get_quorum():
            self.send_accept(req_id, payload["n"])
    
    def send_accept(self, req_id, n):
        value = self.current_value
        
        if req_id in self.promise_values and self.promise_values[req_id]:
            max_n = -1
            max_val = None
            for acc_n, acc_val in self.promise_values[req_id].values():
                if acc_n > max_n:
                    max_n = acc_n
                    max_val = acc_val
            
            if max_val is not None:
                value = max_val
        
        for acceptor_id in self.acceptor_ids:
            self.send(
                dst_id=acceptor_id,
                msg_type=MessageType.PAXOS_ACCEPT,
                payload={"n": n, "value": value},
                request_id=req_id
            )
        
        if req_id in self.promises:
            del self.promises[req_id]
        if req_id in self.promise_values:
            del self.promise_values[req_id]
    
    def handle_prepare(self, msg: Message):
        if not self.is_acceptor:
            return
        
        req_id = msg.request_id
        n = msg.payload["n"]
        
        highest = self.highest_promised.get(req_id, -1)
        
        if n > highest:
            self.highest_promised[req_id] = n
            
            resp = {"n": n}
            
            if req_id in self.accepted:
                acc_n, acc_val = self.accepted[req_id]
                resp["accepted_n"] = acc_n
                resp["accepted_value"] = acc_val
            else:
                resp["accepted_n"] = None
                resp["accepted_value"] = None
            
            self.send(
                dst_id=msg.source_node_id,
                msg_type=MessageType.PAXOS_PROMISE,
                payload=resp,
                request_id=req_id
            )
    
    def handle_accept(self, msg: Message):
        if not self.is_acceptor:
            return
        
        req_id = msg.request_id
        n = msg.payload["n"]
        value = msg.payload["value"]
        
        highest = self.highest_promised.get(req_id, -1)
        
        if n >= highest:
            self.accepted[req_id] = (n, value)
            
            for learner_id in self.learner_ids:
                self.send(
                    dst_id=learner_id,
                    msg_type=MessageType.PAXOS_ACCEPTED,
                    payload={"n": n, "value": value},
                    request_id=req_id
                )
    
    def handle_accepted(self, msg: Message):
        if not self.is_learner:
            return
        
        req_id = msg.request_id
        acceptor_id = msg.source_node_id
        n = msg.payload["n"]
        value = msg.payload["value"]
        
        if req_id not in self.accepted_msgs:
            self.accepted_msgs[req_id] = {}
        
        self.accepted_msgs[req_id][acceptor_id] = (n, value)
        
        self.check_consensus(req_id)
    
    def check_consensus(self, req_id):
        if req_id in self.learned:
            return
        
        if req_id not in self.accepted_msgs:
            return
        
        counts = {}
        for n, value in self.accepted_msgs[req_id].values():
            key = (n, value)
            counts[key] = counts.get(key, 0) + 1
        
        quorum = self.get_quorum()
        for (n, value), count in counts.items():
            if count >= quorum:
                self.learned[req_id] = value
                
                if req_id in self.client_requests:
                    client_id = self.client_requests[req_id]
                    self.send(
                        dst_id=client_id,
                        msg_type=MessageType.PAXOS_DECISION,
                        payload={"value": value},
                        request_id=req_id
                    )
                    del self.client_requests[req_id]
                
                break
    
    def receive(self, msg: Message):
        if msg.msg_type == MessageType.CLIENT_REQUEST:
            self.handle_client_request(msg)
        elif msg.msg_type == MessageType.PAXOS_PREPARE:
            self.handle_prepare(msg)
        elif msg.msg_type == MessageType.PAXOS_PROMISE:
            self.handle_promise(msg)
        elif msg.msg_type == MessageType.PAXOS_ACCEPT:
            self.handle_accept(msg)
        elif msg.msg_type == MessageType.PAXOS_ACCEPTED:
            self.handle_accepted(msg)
