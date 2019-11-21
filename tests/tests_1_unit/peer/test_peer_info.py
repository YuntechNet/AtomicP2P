from atomic_p2p.peer.entity.peer_info import PeerInfo


def test_eq(peer_info):
    p = PeerInfo(peer_info.name, peer_info.role, peer_info.host)
    assert p == peer_info
    p = PeerInfo(peer_info.name + "1", peer_info.role, peer_info.host)
    assert p != peer_info


def test_contains(peer_info):
    assert peer_info.__contains__(peer_info)


def test_str(peer_info):
    name = peer_info.name
    role = peer_info.role
    host = peer_info.host
    assert str(peer_info) == "PeerInfo<name={0}, role={1}, host={2}>".format(
        name, role.value, str(host)
    )
