from time import sleep

from atomic_p2p.peer.entity.peer_status import StatusType


def test_two_peer(switch1, switch2):
    switch1._on_command(["join", "127.0.0.1:{}".format(switch2.server_info.host[1])])
    sleep(3)

    switch1.monitor.verbose = True
    verbose = switch1.monitor._on_command(
        ["manual", "127.0.0.1:{}".format(switch2.server_info.host[1])])
    assert verbose == "Sended a monitor check to: {}".format(
        list(switch2.server_info.host))
        

def test_three_peer(core1, switch1, switch2):
    switch1._on_command(["join", "127.0.0.1:{}".format(core1.server_info.host[1])])
    switch2._on_command(["join", "127.0.0.1:{}".format(core1.server_info.host[1])])
    sleep(5)

    switch1.monitor.verbose = True
    verbose = switch1.monitor._on_command(["manual", "None:sw"])
    assert verbose == "Sended a monitor check to: ['None', 'sw']"
