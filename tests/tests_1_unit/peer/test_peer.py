
def test_init(default_peer):
    assert default_peer.stopped.is_set() == False
    assert default_peer.server.getsockname() == ('0.0.0.0', 8000)

def test_onProcess(default_peer):
    rtn = default_peer.onProcess(['test', 'test2'])
    assert rtn == ''

