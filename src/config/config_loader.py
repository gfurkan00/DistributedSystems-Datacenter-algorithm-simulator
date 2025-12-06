import yaml

from .protocol_config import ProtocolConfig, NodeGroupConfig
from .simulation_config import SimulationConfig
from .network_config import NetworkConfig
from .workload_config import WorkloadConfig

class ConfigLoader:
    
    @staticmethod
    def load(config_path: str) -> SimulationConfig:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)

            network_data = data["network"]
            network_config = NetworkConfig(
                latency_min=network_data["latency_min"],
                latency_max=network_data["latency_max"],
                packet_loss_probability=network_data["packet_loss_probability"],
            )

            protocol_data = data["protocol"]
            node_groups = []
            for node_group in protocol_data["deployment"]["groups"]:
                node_groups.append(NodeGroupConfig(
                    role_type=node_group["role"],
                    start_id=node_group.get("start_id"),
                    count=node_group["count"]
                ))
            protocol_config = ProtocolConfig(
                name=protocol_data["name"],
                settings=protocol_data.get("settings"),
                node_groups=node_groups,
            )

            workload_data = data.get("workload")
            workload_config = WorkloadConfig(
                type=workload_data.get("type", "sequential"),
                start_id=workload_data.get("start_id"),
                clients=workload_data.get("clients", 1),
                settings=workload_data.get("settings"),
            )

            sim_data = data["simulation"]
            return SimulationConfig(
                seed=sim_data.get("seed"),
                output_file=sim_data["output_file"],
                duration=sim_data["duration"],
                network_config=network_config,
                protocol_config=protocol_config,
                workload_config=workload_config,
            )