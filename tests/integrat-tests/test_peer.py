import traceback

def test_link(node):

    assert str(node['core_1'].connectlist[0]) == 'PeerInfo<name={0}, role={1}, host={2}>'.format('switch01', 'sw', str(('127.0.0.1', '8010')))
    assert str(node['core_1'].connectlist[1]) == 'PeerInfo<name={0}, role={1}, host={2}>'.format('switch02', 'sw', str(('127.0.0.1', '8011')))

