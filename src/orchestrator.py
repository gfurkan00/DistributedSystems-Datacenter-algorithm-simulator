import random
from typing import List, Dict

from src.core.logger.logger import Logger, LoggerAPI
from src.core.scheduler.scheduler import Scheduler, SchedulerAPI
from src.core.network.network import Network, NetworkAPI
from src.core.node.client_node import ClientNode
from src.core.node.node import Node
from src.core.utils.utils import MessageType

# NUOVI IMPORT
from src.config.config_loader import ConfigLoader
from src.core.node.node_factory import NodeFactory

def core(configuration_file: str) -> None:
    # 1. Carica Configurazione
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

    # 5. Creazione Nodi Dinamica
    nodes: Dict[int, Node] = {}
    client_node = None  # Variabile per il client

    for node_cfg in config.nodes:
        # Usa la Factory!
        node = NodeFactory.create(node_cfg, network)
        nodes[node.node_id] = node

        # Registra nella rete
        network.register_node(node.node_id, node.receive)
        
        # Se è il client del workload, salviamolo
        if node.node_id == config.workload.client_id:
            client_node = node

    # Check di sicurezza: Se c'è un workload ma il client non esiste -> Errore!
    if config.workload.requests and client_node is None:
        raise ValueError(f"Workload client_id {config.workload.client_id} not found among created nodes! Check your YAML config.")

    # 6. Esegui Workload
    if client_node and config.workload.requests:
        print(f"Starting workload with {len(config.workload.requests)} requests...")
        target_id = config.workload.target_id
        
        for req in config.workload.requests:
            # Per ora inviamo direttamente (ignorando il delay per semplicità)
            # In futuro useremo lo scheduler per rispettare req.delay
            client_node.send(
                dst_id=target_id,
                msg_type=MessageType.CLIENT_REQUEST,
                payload=req.payload
            )

    # 7. Run Simulation
    scheduler.run()

    # 8. Save Logs
    # Usa il path dal config se presente, altrimenti default
    output_path = config.output_file if config.output_file else "simulation_results.csv"
    logger.dump_to_csv(output_path)
    print(f"Logs saved to {output_path}")