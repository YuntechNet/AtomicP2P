from time import sleep


def test_two_link(core1, edge1):
    edge1._on_command(["join", "atomic_p2p.integrattest.org"])
    sleep(4)
    assert edge1.server_info.host in core1.peer_pool
    assert core1.server_info.host in edge1.peer_pool


def test_three_link(core1, edge1, edge2):
    edge1._on_command(["join", "atomic_p2p.integrattest.org"])
    edge2._on_command(["join", "atomic_p2p.integrattest.org"])
    sleep(12)
    assert edge1.server_info.host in core1.peer_pool
    assert edge2.server_info.host in core1.peer_pool

    assert core1.server_info.host in edge1.peer_pool
    assert edge2.server_info.host in edge1.peer_pool

    assert core1.server_info.host in edge2.peer_pool
    assert edge1.server_info.host in edge2.peer_pool
