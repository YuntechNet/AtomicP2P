import time


def test_send(core1, switch1):
    switch1.sendMessage(('127.0.0.1', core1.listenPort), 'join')
    time.sleep(1)
    switch1.onProcess(['send', '127.0.0.1:{}'.format(core1.listenPort), '123'])
    time.sleep(1)
    assert '123' in core1.last_output


def test_broadcast(core1, switch1, switch2):
    switch1.sendMessage(('127.0.0.1', core1.listenPort), 'join')
    switch2.sendMessage(('127.0.0.1', core1.listenPort), 'join')
    time.sleep(3)

    core1.onProcess(['send', 'broadcast:sw', 'ttt'])
    time.sleep(3)
    assert 'ttt' in switch1.last_output
    assert 'ttt' in switch2.last_output
