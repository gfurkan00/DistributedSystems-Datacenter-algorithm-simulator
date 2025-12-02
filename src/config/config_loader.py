import yaml
from typing import Dict, Any
from .simulation_config import SimulationConfig
from .network_config import NetworkConfig
from .node_config import NodeConfig
from .workload_config import WorkloadConfig

class ConfigLoader:
    
    @staticmethod
    def load(config_path: str) -> SimulationConfig:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
            sim_data = data["simulation"]
            net_data = data["network"]
            node_data_list = data["nodes"]
            work_data = data["workload"]

            network = NetworkConfig(
                latency_min=net_data["latency_min"],
                latency_max=net_data["latency_max"],
                packet_loss_prob=net_data.get("packet_loss_prob", 0.0),
            )

            nodes = []
            for node_dict in node_data_list:
                nodes.append(NodeConfig(
                    id=node_dict["id"],
                    type=node_dict["type"],
                    protocol=node_dict.get("protocol"),
                    config=node_dict.get("config"),
                ))
                
            workload = WorkloadConfig(
                clients=work_data["clients"],
                target_id=work_data["target_id"],
                num_requests=work_data["num_requests"],
            )
            
            return SimulationConfig(
                seed=sim_data["seed"],
                duration_seconds=sim_data.get("duration_seconds"),
                output_file=sim_data.get("output_file"),
                network=network,
                nodes=nodes,
                workload=workload,
            )