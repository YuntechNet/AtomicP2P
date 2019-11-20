from time import sleep


def test_send(core1, edge1):
    edge1.join_net(host=core1.server_info.host)
    sleep(5)
    edge1._on_command(["send", "127.0.0.1:{}".format(core1.server_info.host[1]),
                       "123"])
    sleep(8)
    assert "123" in core1.last_output


def test_broadcast(core1, edge1, edge2):
    edge1.join_net(host=core1.server_info.host)
    edge2.join_net(host=core1.server_info.host)
    sleep(5)

    core1._on_command(["send", "broadcast:edge", "ttt"])
    sleep(8)
    assert "ttt" in edge1.last_output, edge1.last_output
    assert "ttt" in edge2.last_output, edge2.last_output
