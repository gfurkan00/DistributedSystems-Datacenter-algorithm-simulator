# DistributedSystems-Datacenter-algorithm-simulator

A discrete-event simulator for datacenter distributed algorithms and consensus protocols.

## Overview
This simulator allows testing and analyzing distributed systems protocols in a controlled environment with configurable network conditions, node topologies, and workloads.

## Supported Protocols
- **Primary-Backup Replication** - Simple replication with one primary and multiple backup nodes
- **Paxos Consensus** - Distributed consensus protocol for agreement among nodes

## Features
- YAML-based configuration
- Configurable network latency and packet loss
- Discrete event scheduling
- CSV logging for analysis
- Multiple node types (Client, Primary, Backup, Paxos)

## Project Structure
```
src/

```

## Usage
```bash
python main.py -c <configuration.yml>
```

## Example Configurations
- `primary_backup.yml` - Primary-backup with 3 backups
- `paxos_basic.yml` - Paxos consensus with 3 nodes
- `test_high_latency.yml` - High latency scenarios
- `test_heavy_workload.yml` - Heavy request load

## Configuration Format
```yaml
simulation:
  seed: 42
  output_file: "output/results.csv"

network:
  latency_min: 0.5
  latency_max: 2.0
  packet_loss_prob: 0.0

nodes:
  - id: 99
    type: "ClientNode"
  - id: 0
    type: "PaxosNode"
    config:
      proposer_ids: [0, 1, 2]
      acceptor_ids: [0, 1, 2]
      learner_ids: [0, 1, 2]

workload:
  type: "sequential"
  client_id: 99
  target_id: 0
  requests:
    - payload: "Request_1"
      delay: 0.0
```

## Output
Simulation results are saved as CSV files containing:
- Timestamp
- Source/destination node IDs
- Event type (send/receive)
- Message type
- Request ID
- Payload
