import pytest


def test_init(default_peer):
    assert default_peer.stopped.is_set() is False
    assert default_peer._Peer__tcp_server.getsockname() == ('0.0.0.0', 8000)


def test_onProcess(default_peer):
    assert default_peer.onProcess(['test', 'test2']) == ''


def test_select_handler(default_peer):
    for (key, value) in default_peer.pkt_handlers.items():
        assert default_peer.select_handler(key) == value
    assert default_peer.select_handler('monitor_check') is not None
    assert default_peer.select_handler('this must be none') is None


def test_handler_unicast_packet(default_peer):
    default_peer.handler_unicast_packet(('1.2.3.4', 1234), 'None')


def test_add_peer_in_net(default_peer, peer_info):
    assert len(default_peer.connectlist) == 0
    default_peer.add_peer_in_net(peer_info)
    assert peer_info in default_peer.connectlist


def test_del_peer_in_net(default_peer, peer_info):
    assert peer_info in default_peer.connectlist
    assert default_peer.del_peer_in_net(peer_info) is True
    assert peer_info not in default_peer.connectlist
    assert default_peer.del_peer_in_net(peer_info) is False
    assert peer_info not in default_peer.connectlist
