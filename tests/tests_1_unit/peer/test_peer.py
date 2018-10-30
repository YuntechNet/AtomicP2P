import pytest


def test_init(default_peer):
    assert default_peer.stopped.is_set() is False
    assert default_peer.server.getsockname() == ('0.0.0.0', 8000)


def test_onProcess(default_peer):
    # assert default_peer.onProcess(['send']) == ''
    assert default_peer.onProcess(['test', 'test2']) == ''


def test_selectHandler(default_peer):
    for (key, value) in default_peer.handler.items():
        assert default_peer.selectHandler(key) == value
    assert default_peer.selectHandler('monitor_check') is not None
    assert default_peer.selectHandler('this must be none') is None


def test_sendMessage(default_peer):
    default_peer.sendMessage(None, 'None')


def test_addConnectlist(default_peer, peer_info):
    assert default_peer.connectlist == []
    default_peer.addConnectlist(peer_info)
    assert peer_info in default_peer.connectlist


def test_getConnectByHost(default_peer, peer_info):
    assert default_peer.getConnectByHost(peer_info.host) == peer_info
    assert default_peer.getConnectByHost('fakehost:1111') is None


def test_getConnectByName(default_peer, peer_info):
    assert default_peer.getConnectByName('this must be none') is None
    assert default_peer.getConnectByName(peer_info.name) == peer_info


def test_removeConnectlist(default_peer, peer_info):
    assert peer_info in default_peer.connectlist
    assert default_peer.removeConnectlist(peer_info) is True
    assert peer_info not in default_peer.connectlist
    assert default_peer.removeConnectlist(peer_info) is False
    assert peer_info not in default_peer.connectlist
