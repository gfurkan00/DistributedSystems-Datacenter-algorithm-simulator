
from src.core.logger import Logger
from src.core.logger.logger_interface import LoggerAPI
from src.core.network import Network, NetworkAPI
from src.core.node import ClientNode
from src.core.scheduler import Scheduler, SchedulerAPI
from src.core.utils import MessageType
from src.protocols.paxos import ProposerNode, AcceptorNode


def core(configuration_file: str) -> None:
    """Entry point for the simulation.

    The configuration file is currently unused – the simulator simply
    spins up a small Paxos deployment:
        * 1 client
        * 1 proposer
        * 5 acceptors
    and sends a few client requests through the system.
    """  # noqa: D401
    logger: LoggerAPI = Logger.create()
    scheduler: SchedulerAPI = Scheduler(logger=logger)
    network: NetworkAPI = Network(scheduler=scheduler, logger=logger, latency_min=0.5, latency_max=2.0)

    # Nodes
    client = ClientNode(node_id=99, network=network)
    acceptor_ids = [1, 2, 3, 4, 5]
    acceptors = [AcceptorNode(node_id=i, network=network) for i in acceptor_ids]
    proposer = ProposerNode(node_id=10, network=network, acceptor_ids=acceptor_ids)

    # Register nodes in the network
    network.register_node(client.node_id, client.receive)
    for acc in acceptors:
        network.register_node(acc.node_id, acc.receive)
    network.register_node(proposer.node_id, proposer.receive)

    # Send a few client requests to the proposer
    for value in ["A", "B", "C", "D", "E", "F"]:
        client.send(dst_id=proposer.node_id, msg_type=MessageType.CLIENT_REQUEST, payload=value)

    # Run the simulation
    scheduler.run()

    # Print and persist logs
    logger.print()
    logger.dump_to_csv("simulation_results_paxos.csv")
