from src.core.logger import Logger
from src.core.logger.logger_interface import LoggerAPI
from src.core.network import Network, NetworkAPI
from src.core.node import ClientNode
from src.core.scheduler import Scheduler, SchedulerAPI
from src.core.utils import MessageType
from src.protocols.lowi import LowiNode
from src.protocols.primary_backup import BackupNode, PrimaryNode


def core(configuration_file: str) -> None:
    logger: LoggerAPI = Logger.create()
    scheduler: SchedulerAPI = Scheduler(logger=logger)
    network: NetworkAPI = Network(scheduler=scheduler, logger=logger, latency_min=0.5, latency_max=2)

    all_lowi_nodes = [0, 1, 2, 3, 4]

    loop_leader_period = 0.2
    timeout_follower_period = 0.5
    timeout_limit = 2.5
    sync_latency = 0.1

    client1 = ClientNode(node_id=99, network=network)
    client2 = ClientNode(node_id=98, network=network)

    leader = LowiNode(node_id=0, network=network, all_nodes=all_lowi_nodes, loop_leader_period=loop_leader_period, timeout_follower_period=timeout_follower_period, timeout_limit=timeout_limit, sync_latency=sync_latency, violation_synchronous_probability=0.001)
    follower1 = LowiNode(node_id=1, network=network, all_nodes=all_lowi_nodes, loop_leader_period=loop_leader_period, timeout_follower_period=timeout_follower_period, timeout_limit=timeout_limit, sync_latency=sync_latency, violation_synchronous_probability=0.001)
    follower2 = LowiNode(node_id=2, network=network, all_nodes=all_lowi_nodes, loop_leader_period=loop_leader_period, timeout_follower_period=timeout_follower_period, timeout_limit=timeout_limit, sync_latency=sync_latency, violation_synchronous_probability=0.001)
    follower3 = LowiNode(node_id=3, network=network, all_nodes=all_lowi_nodes, loop_leader_period=loop_leader_period, timeout_follower_period=timeout_follower_period, timeout_limit=timeout_limit, sync_latency=sync_latency, violation_synchronous_probability=0.001)
    follower4 = LowiNode(node_id=4, network=network, all_nodes=all_lowi_nodes, loop_leader_period=loop_leader_period, timeout_follower_period=timeout_follower_period, timeout_limit=timeout_limit, sync_latency=sync_latency, violation_synchronous_probability=0.001)

    network.register_node(client1.node_id, client1.receive)
    network.register_node(client2.node_id, client2.receive)

    network.register_node(leader.node_id, leader.receive)
    network.register_node(follower1.node_id, follower1.receive)
    network.register_node(follower2.node_id, follower2.receive)
    network.register_node(follower3.node_id, follower3.receive)
    network.register_node(follower4.node_id, follower4.receive)

    #TODO: Se cambia il leader prima che un client invia la request come fa a sapere nuovo leader id
    client1.send(dst_id=leader.node_id, msg_type=MessageType.CLIENT_REQUEST, payload="A")
    client2.send(dst_id=leader.node_id, msg_type=MessageType.CLIENT_REQUEST, payload="B")

    scheduler.run()

    logger.print()
    logger.dump_to_csv("lowi_test.csv")