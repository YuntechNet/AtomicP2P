
from time import sleep


def test_no_peer(core1):
    assert core1._on_command(['list']) == 'There is no peers in current net.'


def test_one_peer(switch1, switch2):
    switch1._on_command(['join', '127.0.0.1:{}'.format(switch2.server_info.host[1])])
    sleep(3)
    
    assert 'Current peers info:' in switch1._on_command(['list'])
    assert 'Current peers info:' in switch2._on_command(['list'])

    switch1._on_command(['leavenet'])
    switch2._on_command(['leavenet'])
    sleep(3)
