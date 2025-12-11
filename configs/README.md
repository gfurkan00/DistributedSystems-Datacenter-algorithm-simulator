# ⚙️ Configuration Guide

The **Datacenter Algorithm Simulator** is purely data-driven. Every aspect of the simulation, from network latency to the specific consensus algorithm and failure injection, is defined in a **YAML** configuration file.

To run a simulation, pass the config file path to the main executable:

```bash
uv run main.py -c your_config.yml
```

---

## 📑 Structure Overview

A configuration file consists of five main sections:

- **simulation:** Global experiment settings.
- **network:** Datacenter network modeling.
- **protocol:** The specific distributed algorithm and node topology.
- **workload:** Client behavior and request generation.
- **failures:** Scheduled fault injection events.

### 1. Common Configuration Modules

These sections are shared across all protocols.

#### Simulation

Controls the execution environment and reproducibility.

| Parameter     | Type     | Description                                                                                             |
|---------------|----------|---------------------------------------------------------------------------------------------------------|
| `duration`    | `int`    | The maximum simulation time (virtual units/ticks)                                                       |
| `output_file` | `string` | Path where the CSV metrics will be saved                                                                |
| `seed`        | `int`    | (Optional) If provided, the simulation is deterministic. If omitted or commented out, the run is random |

---

#### Network

Models the physical layer constraints.

| Parameter                            | Type    | Description                                                                                               |
|--------------------------------------|---------|-----------------------------------------------------------------------------------------------------------|
| `latency_min_wan`                    | `float` | Minimum transmission delay for WAN client communication to datacenter (virtual units/ticks)               |
| `latency_max_wan`                    | `float` | Maximum transmission delay for WAN client communication to datacenter (virtual units/ticks)               |
| `packet_loss_probability_wan`        | `float` | Probability (0.0 to 1.0) of a message being dropped for WAN client communication to datacenter            |
| `latency_min_datacenter`             | `float` | (Optional) Minimum transmission delay for communication with datacenter Hardware (virtual units/ticks)    |
| `latency_max_datacenter`             | `float` | (Optional) Maximum transmission delay for communication with datacenter Hardware (virtual units/ticks)    |
| `packet_loss_probability_datacenter` | `float` | (Optional) Probability (0.0 to 1.0) of a message being dropped for communication with datacenter Hardware |

---

#### Workload

Defines the clients interacting with the system.

| Parameter                 | Type     | Description                                                                     |
|---------------------------|----------|---------------------------------------------------------------------------------|
| `type`                    | `string` | Workload pattern (e.g. `sequential`)                                            |
| `clients`                 | `int`    | Number of client nodes to spawn                                                 |
| `start_id`                | `int`    | (Optional) Starting Integer ID for clients. If omitted, random IDs are assigned |
| `num_requests_per_client` | `int`    | Total requests sent by one client                                               |
| `loop_client_period`      | `float`  | Time interval between client loops                                              |
| `request_timeout_period`  | `float`  | How long a client waits for a response before retrying/failing                  |

---

#### Failures

A list of scheduled events to test fault tolerance.

| Parameter | Type             | Description                                  |
|-----------|------------------|----------------------------------------------|
| `time`    | `float`          | The exact simulation time the failure occurs |
| `action`  | `string`         | The type of failure (e.g. `crash`)           |
| `target`  | `int` or `[int]` | The ID(s) of the node(s) to fail             |

---

### 2. Protocol & Deployment Strategy

The protocol section defines what algorithm runs and how nodes are instantiated.
The simulator uses a flexible Group-based deployment. You can define multiple groups of nodes with specific roles.

```yaml
protocol:
  name: <string>
  deployment:
    groups:
      - role: <string> # Python class name for the node
        count: <int> # How many nodes of this type
        start_id: Optional<int> # (Optional) Starting ID
      - role: <string>
        count: <int>
```

> **Note on Node IDs (start_id)**
>
> - If start_id is provided: Nodes are assigned sequential Integer IDs starting from that number (e.g., 0, 1, 2). This is useful for deterministic testing and targeted failures.
> - If start_id is omitted: Nodes are assigned random UUIDs.

---

### 3. Supported Protocols & Examples

Below are the specific settings and configurations for the currently implemented protocols.

#### 3.1 Primary Backup

A standard replication protocol with one leader (Primary) and multiple followers (Backups).

> **Specific Settings** \
> **replication_factor:** Total number of replicas required.

```yaml
protocol:
  name: "primary_backup"
  settings:
    replication_factor: 3
  deployment:
    groups:
      - role: "PrimaryNode"
        start_id: 0
        count: 1
      - role: "BackupNode"
        start_id: 1
        count: 9
```

---

#### 3.2 LOWI

Looped One-Way Imposition. A protocol designed for datacenter synchrony.

> **Specific Settings**\
> **loop_leader_period:** Frequency of leader loop operations. \
> **timeout_follower_period:** Time before a follower suspects a leader failure. \
> **timeout_limit:** Timeout threshold. \
> **sync_latency:** The assumed synchronous network delay. \
> **violation_synchronous_probability:** Probability that the `sync_latency` assumption is violated.

```yaml
protocol:
  name: "lowi"
  settings:
    loop_leader_period: 0.2
    timeout_follower_period: 0.5
    timeout_limit: 2.5
    sync_latency: 0.1
    violation_synchronous_probability: 0.01
  deployment:
    groups:
      - role: "LowiNode"
        start_id: 0
        count: 10
```

---

#### 3.3 Basic Paxos

A consensus protocol involving Proposers and Acceptors.

```yaml
protocol:
  name: "basic_paxos"
  deployment:
    groups:
      - role: "ProposerNode"
        start_id: 0
        count: 2
      - role: "AcceptorNode"
        start_id: 2
        count: 5
```

> **Note** that specific settings are often handled internally by the topology strategy if not explicitly required in the configuration. This includes not only parameters that are simply not needed, but also those that cannot be provided in advance due to the nature of the topology itself. For example, a primary node automatically inferring all backup_ids, or each LowiNode determining the full set of node ids without requiring them to be manually listed.

---

## 🚀 Full Configuration Template

Use this template to create a new simulation. Uncomment and fill only the protocol section you need.

```yaml
# ==========================================
# 1. SIMULATION & NETWORK (Global)
# ==========================================
simulation:
  # seed: 42  # Uncomment for deterministic runs
  output_file: "output/simulation_results.csv"
  duration: 1000

network:
  latency_min: 0.5
  latency_max: 2.0
  packet_loss_probability: 0.01

# ==========================================
# 2. WORKLOAD (Clients)
# ==========================================
workload:
  type: "sequential"
  clients: 2
  start_id: 100 # Clients will be IDs 100, 101...
  settings:
    num_requests_per_client: 5
    loop_client_period: 2
    request_timeout_period: 5

# ==========================================
# 3. FAILURES (Optional)
# ==========================================
failures:
  - time: 50.0
    action: "crash"
    target: 0 # Targets node with ID 0

# ==========================================
# 4. PROTOCOL (Choose ONE block below)
# ==========================================

# --- OPTION A: PRIMARY BACKUP ---
protocol:
  name: "primary_backup"
  settings:
    replication_factor: 3
  deployment:
    groups:
      - role: "PrimaryNode"
        start_id: 0
        count: 1
      - role: "BackupNode"
        start_id: 1
        count: 5
# --- OPTION B: BASIC PAXOS ---
# protocol:
#   name: "basic_paxos"
#   deployment:
#     groups:
#       - role: "ProposerNode"
#         start_id: 0
#         count: 2
#       - role: "AcceptorNode"
#         start_id: 2
#         count: 5

# --- OPTION C: LOWI ---
# protocol:
#   name: "lowi"
#   settings:
#     loop_leader_period: 0.2
#     timeout_follower_period: 0.5
#     timeout_limit: 2.5
#     sync_latency: 0.1
#     violation_synchronous_probability: 0.01
#   deployment:
#     groups:
#       - role: "LowiNode"
#         start_id: 0
#         count: 5
```

---

## Node Types

| Type           | Protocol       | Role                      |
|----------------|----------------|---------------------------|
| `ClientNode`   | Any            | Sends requests            |
| `PrimaryNode`  | Primary-Backup | Main replica              |
| `BackupNode`   | Primary-Backup | Backup replica            |
| `ProposerNode` | Paxos          | Proposes values           |
| `AcceptorNode` | Paxos          | Accepts/rejects proposals |
| `LowiNode`     | LOWI           | Leader & Follower logic   |

---

## 📖 More Information

- See: Protocol implementations in `../src/protocols/`
- See: Main README file [here](../README.md)
