
def test_init(default_peer):
    assert default_peer.stopped.is_set() == False
    assert default_peer.server.getsockname() == ('0.0.0.0', 8000)

