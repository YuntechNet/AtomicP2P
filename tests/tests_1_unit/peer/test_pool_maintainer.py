from LibreCisco.peer.entity.peer_info import PeerInfo


def test_syncFromDNS(pool_maintainer):
    pool_maintainer.syncFromDNS()
    assert PeerInfo(name='peer_1', role='switch', host=('192.168.1.103', 8000)) in pool_maintainer._servicePeerPool
    assert PeerInfo(name='peer_2', role='switch', host=('192.168.1.104', 8000)) in pool_maintainer._servicePeerPool
    assert PeerInfo(name='peer_3', role='switch', host=('192.168.1.105', 8000)) in pool_maintainer._servicePeerPool
    assert PeerInfo(name='peer_1', role='scheduler', host=('192.168.1.106', 8000)) in pool_maintainer._globalPeerPool
    assert PeerInfo(name='peer_2', role='scheduler', host=('192.168.1.107', 8000)) in pool_maintainer._globalPeerPool
    assert PeerInfo(name='peer_3', role='scheduler', host=('192.168.1.108', 8000)) in pool_maintainer._globalPeerPool


def test_fqdnInfo(pool_maintainer):
    res = pool_maintainer.fqdnInfo('1234')
    assert res == (None, None, None, None)
    res = pool_maintainer.fqdnInfo('192.168.1.103')
    assert res == ('peer_1', 'switch', 'peer_1.switch.yunnms.lalala.org', '192.168.1.103')


def test_forward(pool_maintainer):
    l = pool_maintainer.forward('1234')
    assert l == []
    l = pool_maintainer.forward('peer_1.switch.yunnms.lalala.org')
    assert l[0] == '192.168.1.103'


def test_reverse(pool_maintainer):
    l = pool_maintainer.reverse('1234')
    assert l == []
    l = pool_maintainer.reverse('192.168.1.103')
    assert l[0] == 'peer_1.switch.yunnms.lalala.org.'


def test_srv(pool_maintainer):
    l = pool_maintainer.srv('1234')
    assert l == [0, 0, -1, None]
    l = pool_maintainer.srv('peer_1.switch.yunnms.lalala.org')
    assert l == ['0', '0', '8000', 'peer_1.switch.yunnms.lalala.org.']