# Datacenter Algorithm Simulator

## 📑 Index

- [Description](#-description)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation & Usage](#-installation--usage)
- [Configuration](#-configuration)
- [Authors](#-authors)

---

## 🎯 Description

The **Datacenter Algorithm Simulator** is a flexible and extensible framework designed to simulate distributed algorithms within a datacenter environment.

Testing distributed protocols on real hardware is often costly, time-consuming, and difficult to debug. This project aims to solve this by providing a simulation environment that allows for quick prototyping and performance evaluation of both existing and novel replication algorithms.

---

## 🚀 Features

Based on the requirements for modern distributed systems analysis, this simulator supports:

- **Decoupled Architecture:** High separation between the core simulation engine and protocol implementations, allowing developers to add new protocols by simply defining nodes and a topology strategy.
- **Simple Message Passing:** Protocols use direct send/receive primitives rather than abstract quorum systems.
- **Synchrony & Asynchrony:** Support for modeling both asynchronous message passing and synchronous protocols.
- **Accurate Latency Modeling:** Parameters to model end-host processing and network communication delays suitable for high-performance datacenter settings.
- **Pluggable Protocols:** currently includes implementations for:
  - _Primary Backup Replication_
  - _Basic Paxos_
  - _Looped One-Way Imposition (LOWI)_
- **Failure Injection:** Built-in services to simulate node failures and network partitions.
- **Flexible Configuration:** Entire simulations are driven by YAML configuration files.

---

## 📂 Project Structure

The project is organized to separate the simulation core from specific protocol implementations.

```text
src/
├── config/       # Handles parsing of YAML configuration files
├── core/         # The heart of the simulator
│   ├── network/  # Message passing interface and simulated network layer
│   ├── node/     # Abstract base classes for nodes and clients
│   ├── oracles/  # Handles usefull data such as leader id (which change dynamically)
│   ├── logger/   # Centralized logging system
│   └── scheduler/# Event loop and task scheduling for the simulation
├── protocols/    # Protocol-specific implementations
│   ├── basic_paxos/    # Paxos Proposer/Acceptor nodes & Topology Strategy
│   ├── lowi/           # LOWI nodes & Topology Strategy
│   ├── primary_backup/ # PB nodes & Topology Strategy
│   └── topology_factory# Factory pattern to instantiate the correct protocol strategy
├── service/      # Orchestration services
│   ├── topology/ # Manages the creation and wiring of nodes based on config
│   └── failure/  # Manages simulated failures during runtime
├── metrics/      # Tools for analyzing simulation results (throughput/latency plots)
└── orchestrator.py # Main driver ensuring services work together
```

---

## ⚡ Installation & Usage

This project uses **Python** and manages dependencies using **uv** for high performance.

### Prerequisites

- **Python 3.13+**
- **uv**
  > 📥 [Click here for the official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)

---

### 1. Clone the repository

```bash
git clone https://github.com/gfurkan00/DistributedSystems-Datacenter-algorithm-simulator.git
cd DistributedSystems-Datacenter-algorithm-simulator
```

### 2. Install dependencies

Initialize the virtual environment and sync dependencies:

```bash
uv sync
```

### 3. Activate the Virtual Environment

Depending on your operating system, run:

- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```

### 4. Run a Simulation

To execute the simulator, use `uv run` pointing to the main entry point and passing a configuration file:

```bash
uv run main.py -c configs/your_config_file.yml
```

You can also view all available command-line arguments by running:

```bash
uv run main.py --help
```

---

## ⚙️ Configuration

The simulator is fully data-driven. A single YAML file dictates the topology, the protocol to use, network latency settings, and the workload (client requests).

👉 Click [here](./configs/README.md) for the Detailed Configuration Guide.

---

## 👨‍💻 Authors

- **Luca Fantò** - Research Assistant in Distributed Systems and Cloud (ISIN - Institute of Information Systems and Networking)

- **Furkan Gumus** - Cloud Engineer
