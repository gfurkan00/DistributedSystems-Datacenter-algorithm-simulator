# DistributedSystems-Datacenter-algorithm-simulator
# Paxos Implementation

This branch implements the Paxos consensus protocol for the distributed systems simulator.
Paxos is a consensus algorithm that allows multiple nodes to agree on a single value even with network delays and failures.

## Files
- `paxos_node.py` - Main Paxos implementation
- `messages_updated` - Added Paxos message types
- `node_builder` - Added PaxosNode creation
- `paxos_basic.yml` - Example configuration

## Configuration
```yaml
nodes:
  - id: 0
    type: "PaxosNode"
    config:
      proposer_ids: [0, 1, 2]
      acceptor_ids: [0, 1, 2]
      learner_ids: [0, 1, 2]
```

## Quorum
The system requires a majority of acceptors to reach consensus:
* 3 nodes = 2 required
* 5 nodes = 3 required
* 7 nodes = 4 required
