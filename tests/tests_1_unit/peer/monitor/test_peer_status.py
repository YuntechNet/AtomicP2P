from LibreCisco.peer.monitor.peer_status import StatusType


def test_init(peer_info, peer_status):
    assert peer_status.peer_info == peer_info
    assert peer_status.status == StatusType.PENDING


def test_eq(peer_status, peer_status2):
    assert peer_status == peer_status
    assert peer_status != peer_status2


def test_str(peer_status):
    assert str(peer_status) == 'PeerStatus<host={}, status={}>'.format(
            str(peer_status.peer_info.host), peer_status.status)


def test_toDict(peer_status):
    _dict = peer_status.toDict()
    assert _dict['send_ts'] == peer_status.last_update_ts


def test_update(peer_status):
    assert peer_status.no_response_count == 0
    peer_status.update(status_type=StatusType.PENDING)
    assert peer_status.no_response_count == 1
    assert peer_status.status == StatusType.PENDING
    peer_status.update(status_type=StatusType.UPDATED)
    assert peer_status.no_response_count == 0
    assert peer_status.status == StatusType.UPDATED
