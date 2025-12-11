import os
import random
import time

import src.core.node.client as client
import src.protocols.primary_backup as primary_backup
import src.protocols.lowi as lowi
import src.protocols.basic_paxos as basic_paxos

from src.core.logger.logger import Logger, LoggerAPI
from src.core.oracles import OracleRequest
from src.core.scheduler.scheduler import Scheduler, SchedulerAPI
from src.core.network.network import Network, NetworkAPI
from src.config import ConfigLoader
from src.service.failure import FailureServiceAPI, FailureService
from src.service.topology import TopologyServiceAPI, TopologyService


def _register_nodes_factories():
    client.register()
    primary_backup.register()
    lowi.register()
    basic_paxos.register()

def core(configuration_file: str) -> None:
    _register_nodes_factories()

    config = ConfigLoader.load(configuration_file)

    if config.seed:
        random.seed(config.seed)
    
    logger: LoggerAPI = Logger()
    scheduler: SchedulerAPI = Scheduler()
    
    network: NetworkAPI = Network(
        scheduler=scheduler, 
        logger=logger, 
        network_config=config.network_config
    )

    topology_service: TopologyServiceAPI = TopologyService(network=network)
    topology_service.build_topology(config=config)
    topology_service.register_topology_into_network()
    print(f"Created topology of {len(topology_service.get_topology())} nodes")

    failure_service: FailureServiceAPI = FailureService(scheduler=scheduler, topology_service=topology_service)
    failure_service.schedule_failures(failure_configs=config.failures)

    start_time = time.time()
    scheduler.run(duration=config.duration)
    print("--- %s seconds ---" % (time.time() - start_time))

    print(f"Success requests are {OracleRequest.get_success_request()} of total {OracleRequest.get_total_requests()} requests")
    print(f"Rate success requests / total request {OracleRequest.get_rate_success() * 100}%")
    print(f"Error requests are {OracleRequest.get_error_request()} of total {OracleRequest.get_total_requests()} requests")
    print(f"Rate error requests / total request {OracleRequest.get_rate_error_request() * 100}%")

    output_path = config.output_file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    logger.dump_to_csv(output_path)
    print(f"Logs saved to {output_path}")