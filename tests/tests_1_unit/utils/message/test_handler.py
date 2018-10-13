import pytest

def test_init(handler):
    assert handler.peer == None

def test_onSend(handler):
    with pytest.raises(NotImplementedError):
        handler.onSend()

def test_onRecv(handler):
    with pytest.raises(NotImplementedError):
        handler.onRecv()
