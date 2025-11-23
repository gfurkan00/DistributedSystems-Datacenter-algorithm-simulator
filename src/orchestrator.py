from src.core.logger import Logger
from src.core.logger.logger_interface import LoggerAPI
from src.core.network import Network, NetworkAPI
from src.core.node import ClientNode
from src.core.scheduler import Scheduler, SchedulerAPI
from src.core.utils import MessageType
from src.protocols.primary_backup import BackupNode, PrimaryNode


def core(configuration_file: str) -> None:
    logger: LoggerAPI = Logger.create()
    scheduler: SchedulerAPI = Scheduler(logger=logger)
    network: NetworkAPI = Network(scheduler=scheduler, logger=logger, latency_min=0.5, latency_max=2)

    client = ClientNode(node_id=99, network=network)
    backup1 = BackupNode(node_id=1, network=network)
    backup2 = BackupNode(node_id=2, network=network)
    backup3 = BackupNode(node_id=3, network=network)
    backup4 = BackupNode(node_id=4, network=network)
    backup5 = BackupNode(node_id=5, network=network)
    leader = PrimaryNode(node_id=0, network=network, backup_ids=[backup1.node_id, backup2.node_id, backup3.node_id, backup4.node_id, backup5.node_id])

    network.register_node(client.node_id, client.receive)
    network.register_node(backup1.node_id, backup1.receive)
    network.register_node(backup2.node_id, backup2.receive)
    network.register_node(backup3.node_id, backup3.receive)
    network.register_node(backup4.node_id, backup4.receive)
    network.register_node(backup5.node_id, backup5.receive)
    network.register_node(leader.node_id, leader.receive)

    client.send(dst_id=leader.node_id, msg_type=MessageType.CLIENT_REQUEST, payload="A")
    client.send(dst_id=leader.node_id, msg_type=MessageType.CLIENT_REQUEST, payload="B")
    client.send(dst_id=leader.node_id, msg_type=MessageType.CLIENT_REQUEST, payload="C")
    client.send(dst_id=leader.node_id, msg_type=MessageType.CLIENT_REQUEST, payload="D")
    client.send(dst_id=leader.node_id, msg_type=MessageType.CLIENT_REQUEST, payload="E")
    client.send(dst_id=leader.node_id, msg_type=MessageType.CLIENT_REQUEST, payload="F")

    scheduler.run()

    logger.print()
    logger.dump_to_csv("simulation_results_2.csv")