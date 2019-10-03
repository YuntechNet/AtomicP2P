import pytest


def test_init(handler, default_peer):
    assert handler.peer == default_peer


def test__build_reject_packet(handler):
    packet = handler._build_reject_packet(("1.2.3.4", 5678), **{"reject_data": "test reason"})
    assert packet.data["reject"] == "test reason"
    assert packet.dst == ("1.2.3.4", 5678)


def test_accept_packet(handler):
    with pytest.raises(NotImplementedError):
        handler._build_accept_packet(None)


def test_on_recv_reject_pkt(handler, packet):
    packet = packet.clone()
    packet.set_reject("test reason")
    handler.on_recv_reject_pkt(("1.2.3.4", 5678), packet, None)


def test_on_recv_pkt(handler):
    with pytest.raises(NotImplementedError):
        handler.on_recv_pkt(None, None, None)
