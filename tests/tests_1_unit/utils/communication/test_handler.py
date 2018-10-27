import pytest


def test_init(handler, default_peer):
    assert handler.peer == default_peer


def onSend(handler):
    with pytest.raises(NotImplementedError):
        handler.onSend()


def test_onSendReject(handler):
    message = handler.onSendReject('1.2.3.4:5678', 'test reason')
    assert message._data['reject'] == 'test reason'
    assert message._to == '1.2.3.4:5678'


def test_onSendPkt(handler):
    with pytest.raises(NotImplementedError):
        handler.onSendPkt(None)


def test_onRecvReject(handler):
    handler.onRecvReject('1.2.3.4:5678', {'reject': 'test reason'})


def test_onRecvPkt(handler):
    with pytest.raises(NotImplementedError):
        handler.onRecvPkt(None, None)


def onRecv(handler):
    with pytest.raises(NotImplementedError):
        handler.onRecv()
