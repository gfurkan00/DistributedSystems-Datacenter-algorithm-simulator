import random
from typing import List, Dict

from src.core.logger.logger import Logger, LoggerAPI
from src.core.scheduler.scheduler import Scheduler, SchedulerAPI
from src.core.network.network import Network, NetworkAPI
from src.core.node.client_node import ClientNode
from src.core.node.node import Node
from src.core.utils.utils import MessageType

from src.config.config_loader import ConfigLoader
from src.core.node.node_factory import NodeFactory

def core(configuration_file: str) -> None:
    # 1. Load Configuration
    print(f"Loading configuration from {configuration_file}...")
    config = ConfigLoader.load(configuration_file)

    # 2. Setup Seed
    random.seed(config.seed)
    
    # 3. Setup Core
    logger: LoggerAPI = Logger.create()
    scheduler: SchedulerAPI = Scheduler(logger=logger)
    
    # 4. Setup Network
    network: NetworkAPI = Network(
        scheduler=scheduler, 
        logger=logger, 
        latency_min=config.network.latency_min, 
        latency_max=config.network.latency_max
    )

    # 5. Dynamic Node Creation
    nodes: Dict[int, Node] = {}
    client_node = None

    for node_cfg in config.nodes:
        node = NodeFactory.create(node_cfg, network)
        nodes[node.node_id] = node

        # Register node in the network
        network.register_node(node.node_id, node.receive)
        
        # Save client node for workload execution
        if node.node_id == config.workload.client_id:
            client_node = node

    # Safety check: If workload exists but client is missing -> Error
    if config.workload.requests and client_node is None:
        raise ValueError(f"Workload client_id {config.workload.client_id} not found among created nodes! Check your YAML config.")

    # 6. Execute Workload
    if client_node and config.workload.requests:
        print(f"Starting workload with {len(config.workload.requests)} requests...")
        target_id = config.workload.target_id
        
        for req in config.workload.requests:
            client_node.send(
                dst_id=target_id,
                msg_type=MessageType.CLIENT_REQUEST,
                payload=req.payload
            )

    # 7. Run Simulation
    scheduler.run()

    # 8. Save Logs
    output_path = config.output_file if config.output_file else "simulation_results.csv"
    logger.dump_to_csv(output_path)
    print(f"Logs saved to {output_path}")