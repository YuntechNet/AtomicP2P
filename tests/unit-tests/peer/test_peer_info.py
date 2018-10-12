
def test_contains(peer_info):
    a = []
    a.append(peer_info)
    assert peer_info in a
    a = []
    assert not peer_info in a

def test_str(peer_info):
    name = peer_info.name
    role = peer_info.role
    host = peer_info.host
    assert str(peer_info) == 'PeerInfo<name={0}, role={1}, host={2}>'.format(name, role, str(host))
