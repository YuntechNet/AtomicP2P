from LibreCisco.peer.monitor.peer_status import StatusType


def test_addMonitorlist(default_peer, peer_status):
    assert default_peer.monitor.addMonitorlist(peer_status=peer_status) is True
    assert default_peer.monitor.addMonitorlist(peer_status=peer_status) is \
                                                                          False

def test_removeStatusByHost(default_peer, peer_status):
    monitor = default_peer.monitor
    monitor.removeStatusByHost(peer_status.peer_info.host)
    assert peer_status not in monitor.monitorlist


def test_updateStatusByHost(default_peer, peer_status):
    monitor = default_peer.monitor
    assert monitor.updateStatusByHost(host=peer_status.peer_info.host) is None
