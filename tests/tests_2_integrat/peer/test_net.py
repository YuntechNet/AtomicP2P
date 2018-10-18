import traceback
import time
from LibreCisco.peer.peer_info import PeerInfo


def test_two_link(core1, switch1):
    switch1.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    time.sleep(2)
    assert PeerInfo(
            name=switch1.name, role=switch1.peer_info.role,
            host=('127.0.0.1', switch1.peer_info.host[1])) in core1.connectlist
    assert PeerInfo(
            name=core1.name, role=core1.peer_info.role,
            host=('127.0.0.1', core1.peer_info.host[1])) in switch1.connectlist


def test_three_link(core1, switch1, switch2):
    switch1.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    switch2.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    time.sleep(4)
    assert PeerInfo(
            name=switch1.name, role=switch1.peer_info.role,
            host=('127.0.0.1', switch1.peer_info.host[1])) in core1.connectlist
    assert PeerInfo(
            name=switch2.name, role=switch2.peer_info.role,
            host=('127.0.0.1', switch2.peer_info.host[1])) in core1.connectlist

    assert PeerInfo(
            name=core1.name, role=core1.peer_info.role,
            host=('127.0.0.1', core1.peer_info.host[1])) in switch1.connectlist
    assert PeerInfo(
            name=switch2.name, role=switch2.peer_info.role,
            host=('127.0.0.1', switch2.peer_info.host[1])) in switch1.connectlist

    assert PeerInfo(
            name=core1.name, role=core1.peer_info.role,
            host=('127.0.0.1', core1.peer_info.host[1])) in switch2.connectlist
    assert PeerInfo(
            name=switch1.name, role=switch1.peer_info.role,
            host=('127.0.0.1', switch1.peer_info.host[1])) in switch2.connectlist


def test_mal_two_link(core1, malware_peer):
    malware_peer.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    time.sleep(2)
    assert PeerInfo(
            name=malware_peer.name, role=malware_peer.peer_info.role,
            host=(
                '127.0.0.1',
                malware_peer.peer_info.host[1])) not in core1.connectlist
    assert PeerInfo(
            name=core1.name, role=core1.peer_info.role,
            host=(
                '127.0.0.1',
                core1.peer_info.host[1])) not in malware_peer.connectlist


def test_mal_three_link(core1, switch1, malware_peer):
    switch1.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    malware_peer.sendMessage(('127.0.0.1', core1.peer_info.host[1]), 'join')
    time.sleep(4)
    assert PeerInfo(
            name=switch1.name, role=switch1.peer_info.role,
            host=('127.0.0.1', switch1.peer_info.host[1])) in core1.connectlist
    assert PeerInfo(
            name=malware_peer.name, role=malware_peer.peer_info.role,
            host=(
                '127.0.0.1',
                malware_peer.peer_info.host[1])) not in core1.connectlist

    assert PeerInfo(
            name=core1.name, role=core1.peer_info.role,
            host=('127.0.0.1', core1.peer_info.host[1])) in switch1.connectlist
    assert PeerInfo(
            name=malware_peer.name, role=malware_peer.peer_info.role,
            host=(
                '127.0.0.1',
                malware_peer.peer_info.host[1])) not in switch1.connectlist

    assert PeerInfo(
            name=core1.name, role=core1.peer_info.role,
            host=(
                '127.0.0.1',
                core1.peer_info.host[1])) not in malware_peer.connectlist
    assert PeerInfo(
            name=switch1.name, role=switch1.peer_info.role,
            host=(
                '127.0.0.1',
                switch1.peer_info.host[1])) not in malware_peer.connectlist
