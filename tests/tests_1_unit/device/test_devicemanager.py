import pytest


def test_init(default_peer, default_device_manager):
    assert default_device_manager.peer == default_peer
    assert default_device_manager.devices == []


@pytest.mark.skip()
def test_onProcess(default_device_manager):
    assert default_device_manager.onProcess(['test', 'test2']) == ''
