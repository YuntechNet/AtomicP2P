import time
from atomic_p2p.peer.communication.net import JoinHandler


def test_two_dogs(core1, switch1):
    switch1.join_net(host=core1.server_info.host)
    time.sleep(4)
    assert core1.get_peer_info_by_host(host=switch1.server_info.host) is not None
    assert switch1.get_peer_info_by_host(host=core1.server_info.host) is not None

    max_loop_delay = max(core1.monitor.loopDelay, switch1.monitor.loopDelay)
    max_no_res_count = max(core1.monitor.max_no_response_count,
                           switch1.monitor.max_no_response_count)
    switch1._on_command(["leavenet"])
    time.sleep(5)
    assert core1.get_peer_info_by_host(host=switch1.server_info.host) is None
    assert switch1.get_peer_info_by_host(host=core1.server_info.host) is None


def test_three_dogs(core1, switch1, switch2):
    switch1.join_net(host=core1.server_info.host)
    switch2.join_net(host=core1.server_info.host)
    time.sleep(8)
    assert core1.get_peer_info_by_host(host=switch1.server_info.host) is not None
    assert core1.get_peer_info_by_host(host=switch2.server_info.host) is not None

    assert switch1.get_peer_info_by_host(host=core1.server_info.host) is not None
    assert \
        switch1.get_peer_info_by_host(host=switch2.server_info.host) is not None

    assert switch2.get_peer_info_by_host(host=core1.server_info.host) is not None
    assert \
        switch2.get_peer_info_by_host(host=switch1.server_info.host) is not None

    switch1._on_command(["leavenet"])
    max_loop_delay = max(core1.monitor.loopDelay,
                         switch1.monitor.loopDelay,
                         switch2.monitor.loopDelay)
    max_no_res_count = max(core1.monitor.max_no_response_count,
                           switch1.monitor.max_no_response_count,
                           switch2.monitor.max_no_response_count)
    switch1._on_command(["leavenet"])
    time.sleep(5)

    assert core1.get_peer_info_by_host(host=switch1.server_info.host) is None
    assert core1.get_peer_info_by_host(host=switch2.server_info.host) is not None

    assert switch1.get_peer_info_by_host(host=core1.server_info.host) is None
    assert switch1.get_peer_info_by_host(host=switch2.server_info.host) is None

    assert switch2.get_peer_info_by_host(host=core1.server_info.host) is not None
    assert switch2.get_peer_info_by_host(host=switch1.server_info.host) is None
