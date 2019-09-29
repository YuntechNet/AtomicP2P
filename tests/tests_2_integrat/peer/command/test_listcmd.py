from time import sleep


def test_no_peer(core1):
    assert core1._on_command(["list"]) == "There is no peers in current net."


def test_one_peer(switch1, switch2):
    switch1.join_net(host=switch2.server_info.host)
    sleep(5)
    
    assert "Current peers info:" in switch1._on_command(["list"])
    assert "Current peers info:" in switch2._on_command(["list"])
