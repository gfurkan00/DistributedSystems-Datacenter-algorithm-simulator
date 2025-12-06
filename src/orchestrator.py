import os
import random

import src.core.node.client as client
import src.protocols.primary_backup as primary_backup
import src.protocols.lowi as lowi

from src.core.logger.logger import Logger, LoggerAPI
from src.core.scheduler.scheduler import Scheduler, SchedulerAPI
from src.core.network.network import Network, NetworkAPI
from src.config import ConfigLoader
from src.core.statistics import Statistics
from src.service.topology_service import TopologyService


def _register_nodes_factories():
    client.register()
    primary_backup.register()
    lowi.register()

def core(configuration_file: str) -> None:
    _register_nodes_factories()

    config = ConfigLoader.load(configuration_file)

    if config.seed:
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

    topology_service: TopologyService = TopologyService(network=network)
    topology_service.build_topology(config=config)
    topology_service.register_topology_into_network()
    print(f"Created topology of {len(topology_service.get_topology())} nodes")

    scheduler.run(duration=config.duration)

    output_path = config.output_file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    logger.dump_to_csv(output_path)
    print(f"Logs saved to {output_path}")

    stats = Statistics(logger.get_logs())
    stats.print_report()