from time import sleep


def test_join_net(core1, switch1):
    assert len(core1._Peer__send_queue) == 0
    core1.join_net(host=switch1.server_info.host)
    assert len(core1._Peer__send_queue) == 1
    sleep(5)
    assert switch1.server_info in core1.connectlist
    assert core1.server_info in switch1.connectlist
