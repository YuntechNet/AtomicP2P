import traceback
import time
from LibreCisco.peer.communication.net import JoinHandler
from LibreCisco.peer.entity.peer_info import PeerInfo


def test_two_link(core1, switch1):
    switch1.sendMessage(('127.0.0.1', core1.peer_info.host[1]), JoinHandler.pkt_type)
    time.sleep(2)
    assert switch1.peer_info in core1.connectlist
    assert core1.peer_info in switch1.connectlist


def test_three_link(core1, switch1, switch2):
    switch1.sendMessage(('127.0.0.1', core1.peer_info.host[1]), JoinHandler.pkt_type)
    switch2.sendMessage(('127.0.0.1', core1.peer_info.host[1]), JoinHandler.pkt_type)
    time.sleep(8)
    assert switch1.peer_info in core1.connectlist
    assert switch2.peer_info in core1.connectlist

    assert core1.peer_info in switch1.connectlist
    assert switch2.peer_info in switch1.connectlist

    assert core1.peer_info in switch2.connectlist
    assert switch1.peer_info in switch2.connectlist


def test_mal_two_link(core1, malware_peer):
    malware_peer.sendMessage(('127.0.0.1', core1.peer_info.host[1]), JoinHandler.pkt_type)
    time.sleep(2)
    assert malware_peer.peer_info not in core1.connectlist
    assert core1.connectlist not in malware_peer.connectlist


def test_mal_three_link(core1, switch1, malware_peer):
    switch1.sendMessage(('127.0.0.1', core1.peer_info.host[1]), JoinHandler.pkt_type)
    malware_peer.sendMessage(('127.0.0.1', core1.peer_info.host[1]), JoinHandler.pkt_type)
    time.sleep(8)
    assert switch1.peer_info in core1.connectlist
    assert malware_peer.peer_info not in core1.connectlist

    assert core1.peer_info in switch1.connectlist
    assert malware_peer.peer_info not in switch1.connectlist

    assert core1.peer_info not in malware_peer.connectlist
    assert switch1.peer_info not in malware_peer.connectlist
