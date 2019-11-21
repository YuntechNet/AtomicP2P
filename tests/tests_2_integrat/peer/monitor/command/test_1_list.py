from time import sleep


def test_no_peer(core1):
    assert core1.monitor._on_command(["list"]) == (
        "There is no peer's info in current list"
    )


def test_one_peer(edge1, edge2):
    edge1.join_net(host=edge2.server_info.host)
    sleep(3)

    assert "Current peers status:" in edge1.monitor._on_command(["list"])
    assert "Current peers status:" in edge2.monitor._on_command(["list"])
