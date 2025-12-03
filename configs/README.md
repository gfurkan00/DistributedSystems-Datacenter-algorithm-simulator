# 📁 Configuration Examples

This directory contains YAML configuration files for the Datacenter Algorithm Simulator.

---

## 📚 Available Configurations

### Basic Examples

| File | Protocol | Description | Use Case |
|------|----------|-------------|----------|
| `example_basic.yml` | Primary-Backup | 3 backups, sequential workload | Learning the framework |
| `example_paxos.yml` | Paxos | 5 acceptors, quorum=3 | Paxos baseline |

### LOWI Examples ⭐

| File | Violation % | Description | Use Case |
|------|-------------|-------------|----------|
| `example_lowi_perfect.yml` | 0% | Perfect synchrony | Best-case performance |
| `example_lowi_1pct.yml` | 1% | Realistic datacenter | Production testing |

### Comparison Configs (For Presentation!)

| File | Protocol | Description |
|------|----------|-------------|
| `example_comparison_lowi.yml` | LOWI | Comparison baseline |
| `example_comparison_paxos.yml` | Paxos | Same setup as LOWI |

**Purpose**: Run both configs with same seed/workload → Compare results → Show LOWI performance advantage!

---

## 🎯 YAML Structure

### Required Sections

```yaml
simulation:
  seed: <int>                    # For reproducibility
  output_file: <path>            # Where to save results

network:
  latency_min: <float>           # Microseconds
  latency_max: <float>
  packet_loss_prob: <0.0-1.0>   # Optional
  
  # ⭐ For LOWI only
  synchrony:                     # Optional
    enabled: <bool>
    expected_latency: <float>    # µs
    violation_probability: <0.0-1.0>

nodes:
  - id: <int>                    # Unique node ID
    type: <NodeType>             # ClientNode, PrimaryNode, etc.
    protocol: <string>           # Optional: "primary_backup", "paxos", "lowi"
    config:                      # Optional: protocol-specific config
      <key>: <value>

workload:
  type: "sequential"             # Currently only sequential
  client_id: <int>
  target_id: <int>
  requests:                      # Option 1: List requests
    - payload: <string>
      delay: <float>
  num_requests: <int>            # Option 2: Generate N requests
```

---

## 💡 Key Concepts

### 1. **Synchrony Support** ⭐ (LOWI Innovation!)

```yaml
synchrony:
  enabled: true
  expected_latency: 1.03        # From Nano-consensus paper
  violation_probability: 0.01   # 1% violations
```

**What it does**:
- With probability `1 - violation_probability`: message arrives in exactly `expected_latency` µs
- With probability `violation_probability`: message is delayed (timeout simulation)

**Why it matters**:
- Enables synchronous protocols like LOWI
- First framework to support this!
- Key innovation vs Paxi

### 2. **Protocol-Specific Config**

Different protocols need different parameters:

**Primary-Backup**:
```yaml
config:
  backup_ids: [1, 2, 3]         # List of backup node IDs
```

**Paxos**:
```yaml
config:
  acceptor_ids: [1, 2, 3, 4, 5] # List of acceptor IDs
  quorum_size: 3                # How many need to agree
```

**LOWI**:
```yaml
config:
  follower_ids: [1, 2, 3, 4, 5] # List of follower IDs
  # No quorum needed - one-way imposition!
```

### 3. **Node Types**

| Type | Protocol | Role |
|------|----------|------|
| `ClientNode` | Any | Sends requests |
| `PrimaryNode` | Primary-Backup | Main replica |
| `BackupNode` | Primary-Backup | Backup replica |
| `ProposerNode` | Paxos | Proposes values |
| `AcceptorNode` | Paxos | Accepts/rejects proposals |
| `LOWILeaderNode` | LOWI | Leader (imposes values) |
| `LOWIFollowerNode` | LOWI | Follower (accepts impositions) |

---

## 🚀 Usage Examples

### Run Basic Simulation
```bash
python main.py --config configs/example_basic.yml
```

### Run LOWI with Perfect Synchrony
```bash
python main.py --config configs/example_lowi_perfect.yml
```

### Run Comparison (Demo!)
```bash
# Run LOWI
python main.py --config configs/example_comparison_lowi.yml

# Run Paxos
python main.py --config configs/example_comparison_paxos.yml

# Analyze both
python analyze.py output/comparison_lowi.csv
python analyze.py output/comparison_paxos.csv

# Compare results → Show LOWI advantage!
```

---

## 📊 Creating New Configs

### Template
```yaml
simulation:
  seed: 42
  output_file: "output/my_experiment.csv"

network:
  latency_min: 0.5
  latency_max: 2.0
  packet_loss_prob: 0.0

nodes:
  # Add your nodes here
  - id: 99
    type: "ClientNode"
  
  # ... protocol nodes ...

workload:
  type: "sequential"
  client_id: 99
  target_id: 0
  num_requests: 10
```

### Tips
1. **Start from example**: Copy existing config and modify
2. **Use same seed**: For reproducible experiments
3. **Document purpose**: Add comments explaining your experiment
4. **Name clearly**: `<protocol>_<scenario>_<variation>.yml`

---

## 🎯 Best Practices

### For Testing
- Use `seed: 42` for reproducibility
- Small workload (10-50 requests) for quick tests
- 0% packet loss initially

### For Analysis
- Use `seed: 42` for all comparison configs
- Same workload size across protocols
- Run multiple seeds for statistical significance

### For Demo/Presentation
- Clear naming: `demo_lowi_vs_paxos.yml`
- Medium workload (50-100 requests)
- 0% violations for LOWI (best-case)
- Document expected results in comments

---

## ⚠️ Common Mistakes

### ❌ Different seeds in comparison
```yaml
# Config A
seed: 42

# Config B
seed: 123  # ❌ Different! Results not comparable
```

### ❌ Forgetting synchrony for LOWI
```yaml
# LOWI config without synchrony
network:
  latency_min: 0.5
  latency_max: 2.0
  # ❌ Missing synchrony section!
```

### ❌ Wrong node types
```yaml
# Trying to use Paxos nodes with Primary-Backup
- id: 0
  type: "ProposerNode"       # ❌ Wrong for Primary-Backup!
  protocol: "primary_backup"
```

---

## 📖 More Information

- See: `../ROADMAP_OPTIMIZED.md` for implementation timeline
- See: `../DOCS.md` for framework documentation
- See: Protocol implementations in `../src/protocols/`

---

**Happy experimenting! 🚀**

Focus on LOWI - it's the key innovation! ⭐
