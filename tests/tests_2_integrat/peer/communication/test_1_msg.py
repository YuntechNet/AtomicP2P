from time import sleep


def test_send(core1, switch1):
    switch1.join_net(host=core1.server_info.host)
    sleep(5)
    switch1._on_command(["send", "127.0.0.1:{}".format(core1.server_info.host[1]),
                       "123"])
    sleep(8)
    assert "123" in core1.last_output


def test_broadcast(core1, switch1, switch2):
    switch1.join_net(host=core1.server_info.host)
    switch2.join_net(host=core1.server_info.host)
    sleep(5)

    core1._on_command(["send", "broadcast:sw", "ttt"])
    sleep(8)
    assert "ttt" in switch1.last_output, switch1.last_output
    assert "ttt" in switch2.last_output, switch2.last_output
