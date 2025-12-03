from enum import Enum
from dataclasses import dataclass
from typing import Any


class MessageType(Enum):
    CLIENT_REQUEST = "client_request"
    CLIENT_RESPONSE = "client_response"
    
    PRIMARY_BACKUP_REQUEST = "primary_backup_request"
    PRIMARY_BACKUP_FORWARD = "primary_backup_forward"
    PRIMARY_BACKUP_ACK = "primary_backup_ack"
    PRIMARY_BACKUP_RESPONSE = "primary_backup_response"
    
    PAXOS_PREPARE = "paxos_prepare"
    PAXOS_PROMISE = "paxos_promise"
    PAXOS_ACCEPT = "paxos_accept"
    PAXOS_ACCEPTED = "paxos_accepted"
    PAXOS_DECISION = "paxos_decision"


@dataclass
class Message:
    source_node_id: int
    dest_node_id: int
    msg_type: MessageType
    payload: Any
    request_id: str
    timestamp: float = 0.0
