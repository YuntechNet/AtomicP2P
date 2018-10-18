import time


def test_send(core1, switch1):
    switch1.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    time.sleep(3)
    switch1.onProcess(['send', '127.0.0.1:{}'.format(core1.peer_info.host[1]),
                       '123'])
    time.sleep(5)
    assert '123' in core1.last_output


def test_broadcast(core1, switch1, switch2):
    switch1.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    switch2.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    time.sleep(3)

    core1.onProcess(['send', 'broadcast:sw', 'ttt'])
    time.sleep(5)
    assert 'ttt' in switch1.last_output, switch1.last_output
    assert 'ttt' in switch2.last_output, switch2.last_output