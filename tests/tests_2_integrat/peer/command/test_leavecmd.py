import pytest
from time import sleep


def test_onProcess(switch1, switch2):
    switch1.onProcess(["join", "127.0.0.1:{}".format(switch2.server_info.host[1])])
    sleep(3)
    switch1.onProcess(["leavenet"])
    sleep(3)
    assert switch1.peer_pool == {}
    assert switch2.peer_pool == {}
