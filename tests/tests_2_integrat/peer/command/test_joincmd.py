from time import sleep


def test_join_with_host(core1, edge1):
    assert len(core1.send_queue) == 0
    host = "{}:{}".format(edge1.server_info.host[0], edge1.server_info.host[1])
    core1._on_command(["join", host])
    assert len(core1.send_queue) == 1
    sleep(5)
    assert edge1.server_info in core1.connectlist
    assert core1.server_info in edge1.connectlist


def test_join_net_by_DNS(core1, edge1):
    assert len(core1.send_queue) == 0
    core1._on_command(["join", "atomic_p2p.integrattest.org"])
    assert len(core1.send_queue) == 1
    sleep(5)
    assert edge1.server_info in core1.connectlist
    assert core1.server_info in edge1.connectlist
