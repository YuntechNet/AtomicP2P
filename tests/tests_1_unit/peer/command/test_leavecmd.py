
def test_onProcess(default_peer, peer_info):
    if default_peer.connectlist == []:
        default_peer.addConnectlist(peer_info)
        default_peer.onProcess(['leavenet'])
        assert default_peer.connectlist == []
    else:
        copyConn = default_peer.connectlist.clone()
        default_peer.onProcess(['leavenet'])
        assert default_peer.connectlist == []
        default_peer.connectlist = copyConn
