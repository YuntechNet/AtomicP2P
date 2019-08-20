from time import sleep

from atomic_p2p.peer.entity.peer_status import StatusType


def test_empty_list(switch1, switch2):
    switch1.join_net(host=switch2.server_info.host)
    sleep(3)

    switch1.monitor._on_command(["reset"])
    assert switch1.get_peer_info_by_host(
        host=switch2.server_info.host).status.status == StatusType.PENDING
    

def test_not_empty_list(switch1, switch2):
    switch1.join_net(host=switch2.server_info.host)
    sleep(3)

    switch1.monitor._on_command(["reset", "switch2"])
