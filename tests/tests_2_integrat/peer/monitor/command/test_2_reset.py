from time import sleep

from atomic_p2p.peer.entity.peer_status import StatusType


def test_empty_list(edge1, edge2):
    edge1.join_net(host=edge2.server_info.host)
    sleep(3)

    edge1.monitor._on_command(["reset"])
    assert edge1.get_peer_info_by_host(
        host=edge2.server_info.host).status.status == StatusType.PENDING
    

def test_not_empty_list(edge1, edge2):
    edge1.join_net(host=edge2.server_info.host)
    sleep(3)

    edge1.monitor._on_command(["reset", "edge2"])
