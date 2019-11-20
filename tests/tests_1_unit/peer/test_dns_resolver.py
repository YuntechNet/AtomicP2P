from atomic_p2p.peer.entity import PeerInfo, PeerRole


def test_sync_from_DNS(dns_resolver):
    res = dns_resolver.sync_from_DNS(current_host=("0.0.0.0", 8000), domain="atomic_p2p.unittest.org")
    assert PeerInfo(name="peer_1", role=PeerRole.CORE, host=("192.168.2.103", 8000)) in res
    assert PeerInfo(name="peer_2", role=PeerRole.CORE, host=("192.168.2.104", 8000)) in res
    assert PeerInfo(name="peer_3", role=PeerRole.CORE, host=("192.168.2.105", 8000)) in res
    assert PeerInfo(name="peer_1", role=PeerRole.EDGE, host=("192.168.2.106", 8000)) in res
    assert PeerInfo(name="peer_2", role=PeerRole.EDGE, host=("192.168.2.107", 8000)) in res
    assert PeerInfo(name="peer_3", role=PeerRole.EDGE, host=("192.168.2.108", 8000)) in res


def test_change_ns(dns_resolver):
    dns_resolver.change_ns(ns=["192.168.100.200"])
    assert dns_resolver._ns == ["192.168.100.200"]


def test_forward(dns_resolver):
    l = dns_resolver.forward("1234")
    assert l == []
    l = dns_resolver.forward("peer_1.core.atomic_p2p.unittest.org")
    assert l[0] == "192.168.2.103"


def test_reverse(dns_resolver):
    l = dns_resolver.reverse("1234")
    assert l == []
    l = dns_resolver.reverse("192.168.2.103")
    assert l[0] == "peer_1.core.atomic_p2p.unittest.org."


def test_srv(dns_resolver):
    l = dns_resolver.srv("1234")
    assert l == (0, 0, -1, None)
    l = dns_resolver.srv("peer_1.core.atomic_p2p.unittest.org")
    assert l == ("0", "0", "8000", "peer_1.core.atomic_p2p.unittest.org.")