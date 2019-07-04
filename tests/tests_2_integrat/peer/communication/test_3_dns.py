from time import sleep


def test_two_link(core1, switch1):
    switch1._on_command(["join", "atomic_p2p.integrattest.org"])
    sleep(4)
    assert switch1.server_info.host in core1.peer_pool
    assert core1.server_info.host in switch1.peer_pool


def test_three_link(core1, switch1, switch2):
    switch1._on_command(["join", "atomic_p2p.integrattest.org"])
    switch2._on_command(["join", "atomic_p2p.integrattest.org"])
    sleep(8)
    assert switch1.server_info.host in core1.peer_pool
    assert switch2.server_info.host in core1.peer_pool

    assert core1.server_info.host in switch1.peer_pool
    assert switch2.server_info.host in switch1.peer_pool

    assert core1.server_info.host in switch2.peer_pool
    assert switch1.server_info.host in switch2.peer_pool
