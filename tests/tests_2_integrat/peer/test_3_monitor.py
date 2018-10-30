import time


def test_two_dogs(core1, switch1):
    switch1.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    time.sleep(4)
    assert core1.monitor.getStatusByHost(switch1.peer_info.host)[0] != None
    assert switch1.monitor.getStatusByHost(core1.peer_info.host)[0] != None

    max_loop_delay = max(core1.monitor.loopDelay, switch1.monitor.loopDelay)
    max_no_res_count = max(core1.monitor.max_no_response_count,
                           switch1.monitor.max_no_response_count)
    switch1.onProcess(['leavenet'])
    time.sleep(max_loop_delay * (max_no_res_count + 2))
    assert core1.monitor.getStatusByHost(switch1.peer_info.host)[0] == None
    assert switch1.monitor.getStatusByHost(core1.peer_info.host)[0] == None


def test_three_dogs(core1, switch1, switch2):
    switch1.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    switch2.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    time.sleep(8)
    assert core1.monitor.getStatusByHost(switch1.peer_info.host)[0] != None
    assert core1.monitor.getStatusByHost(switch2.peer_info.host)[0] != None

    assert switch1.monitor.getStatusByHost(core1.peer_info.host)[0] != None
    assert switch1.monitor.getStatusByHost(switch2.peer_info.host)[0] != None

    assert switch2.monitor.getStatusByHost(core1.peer_info.host)[0] != None
    assert switch2.monitor.getStatusByHost(switch1.peer_info.host)[0] != None

    switch1.onProcess(['leavenet'])
    max_loop_delay = max(core1.monitor.loopDelay,
                         switch1.monitor.loopDelay,
                         switch2.monitor.loopDelay)
    max_no_res_count = max(core1.monitor.max_no_response_count,
                           switch1.monitor.max_no_response_count,
                           switch2.monitor.max_no_response_count)
    switch1.onProcess(['leavenet'])
    time.sleep(max_loop_delay * (max_no_res_count + 5))

    assert core1.monitor.getStatusByHost(switch1.peer_info.host)[0] == None
    assert core1.monitor.getStatusByHost(switch2.peer_info.host)[0] != None

    assert switch1.monitor.getStatusByHost(core1.peer_info.host)[0] == None
    assert switch1.monitor.getStatusByHost(switch2.peer_info.host)[0] == None

    assert switch2.monitor.getStatusByHost(core1.peer_info.host)[0] != None
    assert switch2.monitor.getStatusByHost(switch1.peer_info.host)[0] == None
