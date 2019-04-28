from LibreCisco.peer.entity.peer_info import PeerInfo


def test_sync_from_DNS(dns_resolver):
    res = dns_resolver.sync_from_DNS(current_host=('0.0.0.0', 8000), domain='yunnms.test.org')
    assert PeerInfo(name='peer_1', role='switch', host=('192.168.2.103', 8000)) in res
    assert PeerInfo(name='peer_2', role='switch', host=('192.168.2.104', 8000)) in res
    assert PeerInfo(name='peer_3', role='switch', host=('192.168.2.105', 8000)) in res
    assert PeerInfo(name='peer_1', role='scheduler', host=('192.168.2.106', 8000)) in res
    assert PeerInfo(name='peer_2', role='scheduler', host=('192.168.2.107', 8000)) in res
    assert PeerInfo(name='peer_3', role='scheduler', host=('192.168.2.108', 8000)) in res


def test_get_fqdn_info(dns_resolver):
    res = dns_resolver.get_fqdn_info('1234')
    assert res == (None, None, None, None)
    res = dns_resolver.get_fqdn_info('192.168.2.103')
    assert res == ('peer_1', 'switch', 'peer_1.switch.yunnms.test.org', '192.168.2.103')


def test_forward(dns_resolver):
    l = dns_resolver.forward('1234')
    assert l == []
    l = dns_resolver.forward('peer_1.switch.yunnms.test.org')
    assert l[0] == '192.168.2.103'


def test_reverse(dns_resolver):
    l = dns_resolver.reverse('1234')
    assert l == []
    l = dns_resolver.reverse('192.168.2.103')
    assert l[0] == 'peer_1.switch.yunnms.test.org.'


def test_srv(dns_resolver):
    l = dns_resolver.srv('1234')
    assert l == [0, 0, -1, None]
    l = dns_resolver.srv('peer_1.switch.yunnms.test.org')
    assert l == ['0', '0', '8000', 'peer_1.switch.yunnms.test.org.']