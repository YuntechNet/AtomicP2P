from time import sleep

from atomic_p2p.peer.entity.peer_status import StatusType


def test_two_peer(edge1, edge2):
    edge1.join_net(host=edge2.server_info.host)
    sleep(3)

    edge1.monitor.verbose = True
    verbose = edge1.monitor._on_command(
        ["manual", "127.0.0.1:{}".format(edge2.server_info.host[1])])
    assert verbose == "Sended a monitor check to: {}".format(
        list(edge2.server_info.host))
        

def test_three_peer(core1, edge1, edge2):
    edge1.join_net(host=core1.server_info.host)
    edge2.join_net(host=core1.server_info.host)
    sleep(8)

    edge1.monitor.verbose = True
    verbose = edge1.monitor._on_command(["manual", "None:edge"])
    assert verbose == "Sended a monitor check to: ['None', 'edge']"
