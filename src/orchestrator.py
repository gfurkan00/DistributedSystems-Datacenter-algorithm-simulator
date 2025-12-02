import random
from typing import List, Dict, Any

from src.core.logger.logger import Logger, LoggerAPI
from src.core.scheduler.scheduler import Scheduler, SchedulerAPI
from src.core.network.network import Network, NetworkAPI
from src.core.node.node import Node
from src.core.utils.utils import MessageType

from src.config.config_loader import ConfigLoader
from src.core.node.node_factory import NodeFactory

import src.core.node as core_nodes
import src.protocols.primary_backup as primary_backup

def register_nodes():
    core_nodes.register()
    primary_backup.register()

def core(configuration_file: str) -> None:
    register_nodes()

    print(f"Loading configuration from {configuration_file}...")
    config = ConfigLoader.load(configuration_file)

    random.seed(config.seed)
    
    logger: LoggerAPI = Logger.create()
    scheduler: SchedulerAPI = Scheduler(logger=logger)
    
    network: NetworkAPI = Network(
        scheduler=scheduler, 
        logger=logger, 
        latency_min=config.network.latency_min, 
        latency_max=config.network.latency_max
    )

    nodes: Dict[int, Node] = {}

    for node_cfg in config.nodes:
        node = NodeFactory.create(node_cfg, network)
        nodes[node.node_id] = node

        network.register_node(node.node_id, node.receive)

    if config.workload.clients:
        print(f"Starting workload with {config.workload.num_requests} requests per client...")
        target_id = config.workload.target_id
        
        for client_id in config.workload.clients:
            if client_id not in nodes:
                print(f"Warning: Client {client_id} not found in nodes.")
                continue
            
            client = nodes[client_id]
            for i in range(config.workload.num_requests):
                payload = f"Req_{client_id}_{i}"
                client.send(
                    dst_id=target_id,
                    msg_type=MessageType.CLIENT_REQUEST,
                    payload=payload
                )

    scheduler.run()

    output_path = config.output_file if config.output_file else "simulation_results.csv"
    logger.dump_to_csv(output_path)
    print(f"Logs saved to {output_path}")

    from src.core.statistics import Statistics
    stats = Statistics(logger.get_logs())
    stats.print_report()