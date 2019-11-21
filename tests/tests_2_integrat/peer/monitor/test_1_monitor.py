from time import sleep


def test_two_dogs(core1, edge1):
    edge1.join_net(host=core1.server_info.host)
    sleep(4)
    assert core1.get_peer_info_by_host(host=edge1.server_info.host) is not None
    assert edge1.get_peer_info_by_host(host=core1.server_info.host) is not None

    max_loop_delay = max(core1.monitor.loopDelay, edge1.monitor.loopDelay)
    max_no_res_count = (
        max(core1.monitor.max_no_response_count, edge1.monitor.max_no_response_count)
        + 1
    )

    edge1_peer_pool = edge1.peer_pool
    edge1.peer_pool = {}
    sleep(max_loop_delay * max_no_res_count)
    assert core1.get_peer_info_by_host(host=edge1.server_info.host) is None
    assert edge1.get_peer_info_by_host(host=core1.server_info.host) is None
    edge1.peer_pool = edge1_peer_pool


def test_three_dogs(core1, edge1, edge2):
    edge1.join_net(host=core1.server_info.host)
    edge2.join_net(host=core1.server_info.host)
    sleep(8)
    assert core1.get_peer_info_by_host(host=edge1.server_info.host) is not None
    assert core1.get_peer_info_by_host(host=edge2.server_info.host) is not None

    assert edge1.get_peer_info_by_host(host=core1.server_info.host) is not None
    assert edge1.get_peer_info_by_host(host=edge2.server_info.host) is not None

    assert edge2.get_peer_info_by_host(host=core1.server_info.host) is not None
    assert edge2.get_peer_info_by_host(host=edge1.server_info.host) is not None

    max_loop_delay = max(
        core1.monitor.loopDelay, edge1.monitor.loopDelay, edge2.monitor.loopDelay
    )
    max_no_res_count = (
        max(
            core1.monitor.max_no_response_count,
            edge1.monitor.max_no_response_count,
            edge2.monitor.max_no_response_count,
        )
        + 1
    )

    edge1_peer_pool = edge1.peer_pool
    edge1.peer_pool = {}
    sleep(max_loop_delay * max_no_res_count)
    assert core1.get_peer_info_by_host(host=edge1.server_info.host) is None
    assert core1.get_peer_info_by_host(host=edge2.server_info.host) is not None

    assert edge1.get_peer_info_by_host(host=core1.server_info.host) is None
    assert edge1.get_peer_info_by_host(host=edge2.server_info.host) is None

    assert edge2.get_peer_info_by_host(host=core1.server_info.host) is not None
    assert edge2.get_peer_info_by_host(host=edge1.server_info.host) is None
    edge1.peer_pool = edge1_peer_pool
