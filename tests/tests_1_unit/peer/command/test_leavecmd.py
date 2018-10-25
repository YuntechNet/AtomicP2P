
def test_onProcess(default_peer, peer_info):
    if default_peer.connectlist == []:
        default_peer.addConnectlist(peer_info)
        default_peer.onProcess(['leavenet'])
        assert default_peer.connectlist == []
        assert default_peer.watchdog.watchdoglist == []
    else:
        copyConn = default_peer.connectlist.copy()
        copyStatus = default_peer.watchdog.watchdoglist.copy()
        default_peer.onProcess(['leavenet'])
        assert default_peer.connectlist == []
        assert default_peer.watchdog.watchdoglist == []
        default_peer.connectlist = copyConn
        default_peer.watchdog.watchdoglist = copyStatus
