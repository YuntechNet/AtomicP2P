import pytest


def test_init(handler):
    assert handler.peer is None


def onSend(handler):
    with pytest.raises(NotImplementedError):
        handler.onSend()


def test_onSendReject(handler):
    with pytest.raises(NotImplementedError):
        handler.onSendReject(None, None)


def test_onSendPkt(handler):
    with pytest.raises(NotImplementedError):
        handler.onSendPkt(None)


def test_onRecvReject(handler):
    with pytest.raises(NotImplementedError):
        handler.onRecvReject(None, None)


def test_onRecvPkt(handler):
    with pytest.raises(NotImplementedError):
        handler.onRecvPkt(None, None)


def onRecv(handler):
    with pytest.raises(NotImplementedError):
        handler.onRecv()
