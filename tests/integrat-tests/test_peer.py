import traceback
import time
from peer.peer_info import PeerInfo

def test_two_link(core1, switch1):
    switch1.sendMessage(('127.0.0.1', core1.listenPort), 'join')
    time.sleep(2)
    assert PeerInfo(name=switch1.name, role=switch1.role, host=('127.0.0.1', switch1.listenPort)) in core1.connectlist
    assert PeerInfo(name=core1.name, role=core1.role, host=('127.0.0.1', core1.listenPort)) in switch1.connectlist

def test_three_link(core1, switch1, switch2):
    switch1.sendMessage(('127.0.0.1', core1.listenPort), 'join')
    switch2.sendMessage(('127.0.0.1', core1.listenPort), 'join')
    time.sleep(4)
    assert PeerInfo(name=switch1.name, role=switch1.role, host=('127.0.0.1', switch1.listenPort)) in core1.connectlist
    assert PeerInfo(name=switch2.name, role=switch2.role, host=('127.0.0.1', switch2.listenPort)) in core1.connectlist

    assert PeerInfo(name=core1.name, role=core1.role, host=('127.0.0.1', core1.listenPort)) in switch1.connectlist
    assert PeerInfo(name=switch2.name, role=switch2.role, host=('127.0.0.1', switch2.listenPort)) in switch1.connectlist

    assert PeerInfo(name=core1.name, role=core1.role, host=('127.0.0.1', core1.listenPort)) in switch2.connectlist
    assert PeerInfo(name=switch1.name, role=switch1.role, host=('127.0.0.1', switch1.listenPort)) in switch2.connectlist

def test_message(core1, switch1):
    switch1.sendMessage(('127.0.0.1', core1.listenPort), 'join')
    time.sleep(1)
    switch1.sendMessage(('127.0.0.1', core1.listenPort), 'message', **{'msg': '123'})
    time.sleep(1)
    assert core1.last_output.endswith('123')

def test_broadcast(core1, switch1, switch2):
    switch1.sendMessage(('127.0.0.1', core1.listenPort), 'join')
    switch2.sendMessage(('127.0.0.1', core1.listenPort), 'join')
    time.sleep(4)

    data = {
        'role': 'sw',
        'msg': 'ttt'
    }
    for each in core1.connectlist:
        core1.sendMessage(each.host, 'broadcast', **data)
    time.sleep(4)
    assert switch1.last_output.endswith('ttt')
    assert switch2.last_output.endswith('ttt')
