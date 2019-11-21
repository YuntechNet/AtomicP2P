from time import sleep


def test_two_link(core1, edge1):
    edge1.join_net(host=core1.server_info.host)
    sleep(4)
    assert edge1.server_info in core1.connectlist
    assert core1.server_info in edge1.connectlist


def test_three_link(core1, edge1, edge2):
    edge1.join_net(host=core1.server_info.host)
    edge2.join_net(host=core1.server_info.host)
    sleep(8)
    assert edge1.server_info in core1.connectlist
    assert edge2.server_info in core1.connectlist

    assert core1.server_info in edge1.connectlist
    assert edge2.server_info in edge1.connectlist

    assert core1.server_info in edge2.connectlist
    assert edge1.server_info in edge2.connectlist


def test_mal_two_link(core1, malware_peer):
    malware_peer.join_net(host=core1.server_info.host)
    sleep(2)
    assert malware_peer.server_info not in core1.connectlist
    assert core1.connectlist not in malware_peer.connectlist


def test_mal_three_link(core1, edge1, malware_peer):
    edge1.join_net(host=core1.server_info.host)
    malware_peer.join_net(host=core1.server_info.host)
    sleep(8)
    assert edge1.server_info in core1.connectlist
    assert malware_peer.server_info not in core1.connectlist

    assert core1.server_info in edge1.connectlist
    assert malware_peer.server_info not in edge1.connectlist

    assert core1.server_info not in malware_peer.connectlist
    assert edge1.server_info not in malware_peer.connectlist
