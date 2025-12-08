# DistributedSystems-Datacenter-algorithm-simulator
## Paxos implementation assumptions

- We implement a **single-decree Paxos** instance (agreement on one value).
- There is a **single fixed leader/proposer** (node 0). Other nodes never start proposals.
- All replicas act as **acceptors**; the leader is also the **learner**.
- The network is **reliable**: messages are neither lost, duplicated nor reordered.
- Nodes do **not crash** and there are no Byzantine behaviours.
- At any time there is at most **one client request** in the system; requests are processed sequentially.
- We do not model timeouts or leader election. If the leader fails, progress is not guaranteed.
- We assume **bounded message delays**, but we do not model congestion or retransmissions.
