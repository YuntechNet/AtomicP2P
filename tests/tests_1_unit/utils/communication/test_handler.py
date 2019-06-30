import pytest


def test_init(handler, default_peer):
    assert handler.peer == default_peer


def test_on_send_reject_pkt(handler):
    packet = handler.on_send_reject_pkt(("1.2.3.4", 5678), **{"reject_data": "test reason"})
    assert packet.data["reject"] == "test reason"
    assert packet.dst == ("1.2.3.4", 5678)


def test_on_send_pkt(handler):
    with pytest.raises(NotImplementedError):
        handler.on_send_pkt(None)


def test_on_recv_reject_pkt(handler, packet):
    packet = packet.clone()
    packet.set_reject("test reason")
    handler.on_recv_reject_pkt(("1.2.3.4", 5678), packet, None)


def test_on_recv_pkt(handler):
    with pytest.raises(NotImplementedError):
        handler.on_recv_pkt(None, None, None)
