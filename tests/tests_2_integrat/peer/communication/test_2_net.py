from time import sleep

from atomic_p2p.peer.entity.peer_info import PeerInfo


def test_two_link(core1, switch1):
    switch1.join_net(host=core1.server_info.host)
    sleep(4)
    assert switch1.server_info in core1.connectlist
    assert core1.server_info in switch1.connectlist


def test_three_link(core1, switch1, switch2):
    switch1.join_net(host=core1.server_info.host)
    switch2.join_net(host=core1.server_info.host)
    sleep(8)
    assert switch1.server_info in core1.connectlist
    assert switch2.server_info in core1.connectlist

    assert core1.server_info in switch1.connectlist
    assert switch2.server_info in switch1.connectlist

    assert core1.server_info in switch2.connectlist
    assert switch1.server_info in switch2.connectlist


def test_mal_two_link(core1, malware_peer):
    malware_peer.join_net(host=core1.server_info.host)
    sleep(2)
    assert malware_peer.server_info not in core1.connectlist
    assert core1.connectlist not in malware_peer.connectlist


def test_mal_three_link(core1, switch1, malware_peer):
    switch1.join_net(host=core1.server_info.host)
    malware_peer.join_net(host=core1.server_info.host)
    sleep(8)
    assert switch1.server_info in core1.connectlist
    assert malware_peer.server_info not in core1.connectlist

    assert core1.server_info in switch1.connectlist
    assert malware_peer.server_info not in switch1.connectlist

    assert core1.server_info not in malware_peer.connectlist
    assert switch1.server_info not in malware_peer.connectlist
