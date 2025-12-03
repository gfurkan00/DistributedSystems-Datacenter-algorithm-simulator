import os
import random

import src.core.node as core_nodes
import src.protocols.primary_backup as primary_backup
import src.protocols.lowi as lowi

from src.core.logger.logger import Logger, LoggerAPI
from src.core.node import ClientNode
from src.core.scheduler.scheduler import Scheduler, SchedulerAPI
from src.core.network.network import Network, NetworkAPI
from src.core.utils import Oracle, NodeIDGenerator
from src.core.utils.utils import MessageType
from src.config.config_loader import ConfigLoader
from src.core.statistics import Statistics
from src.protocols.topology_factory import TopologyBuilderFactory


def register_nodes():
    core_nodes.register()
    primary_backup.register()
    lowi.register()

def core(configuration_file: str) -> None:
    register_nodes()

    print(f"Loading configuration from {configuration_file}...")
    config = ConfigLoader.load(configuration_file)

    random.seed(config.seed)
    
    logger: LoggerAPI = Logger()
    scheduler: SchedulerAPI = Scheduler(logger=logger)
    
    network: NetworkAPI = Network(
        scheduler=scheduler, 
        logger=logger, 
        latency_min=config.network_config.latency_min,
        latency_max=config.network_config.latency_max,
        packet_loss_probability=config.network_config.packet_loss_probability
    )

    print(f"Building nodes topology for protocol: {config.protocol_config.name}")
    topology_strategy = TopologyBuilderFactory.get_strategy(config.protocol_config.name)
    created_nodes_list = topology_strategy.build(network, config.protocol_config)
    for node in created_nodes_list:
        network.register_node(node_id=node.node_id, receiver_callback=node.receive)


    if config.workload_config.clients > 0:
        target_id = Oracle.get_leader_id()

        for _ in range(config.workload_config.clients):
            client_node_id = NodeIDGenerator.generate()
            client = ClientNode(node_id=client_node_id, network=network)
            network.register_node(node_id=client_node_id, receiver_callback=client.receive)

            for request_id in range(config.workload_config.num_requests_per_client):
                payload = f"Client_{client_node_id}_Req_{request_id}"
                client.send(dst_id=target_id, msg_type=MessageType.CLIENT_REQUEST, payload=payload)

    scheduler.run(duration=500)

    output_path = config.output_file if config.output_file else "output/simulation.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    logger.dump_to_csv(output_path)
    print(f"Logs saved to {output_path}")

    stats = Statistics(logger.get_logs())
    stats.print_report()