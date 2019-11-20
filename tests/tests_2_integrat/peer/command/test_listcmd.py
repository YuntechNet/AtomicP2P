from time import sleep


def test_no_peer(core1):
    assert core1._on_command(["list"]) == "There is no peers in current net."


def test_one_peer(edge1, edge2):
    edge1.join_net(host=edge2.server_info.host)
    sleep(5)
    
    assert "Current peers info:" in edge1._on_command(["list"])
    assert "Current peers info:" in edge2._on_command(["list"])
