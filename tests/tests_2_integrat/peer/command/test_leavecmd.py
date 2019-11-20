import pytest
from time import sleep


def test__on_command(edge1, edge2):
    edge1.join_net(host=edge2.server_info.host)
    sleep(3)
    edge1._on_command(["leavenet"])
    sleep(3)
    assert edge1.peer_pool == {}
    assert edge2.peer_pool == {}
