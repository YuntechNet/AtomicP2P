import pytest
from time import sleep


def test__on_command(switch1, switch2):
    switch1._on_command(['join', '127.0.0.1:{}'.format(switch2.server_info.host[1])])
    sleep(3)
    switch1._on_command(['leavenet'])
    sleep(3)
    assert switch1.peer_pool == {}
    assert switch2.peer_pool == {}
