import pytest


def test_pauseCmd(default_peer):
    assert default_peer.monitor.pause is False
    default_peer.monitor.onProcess(['pause'])
    assert default_peer.monitor.pause is True
    default_peer.monitor.onProcess(['pause'])
    assert default_peer.monitor.pause is False


def test_periodCmd(default_peer):
    origin = default_peer.monitor.loopDelay
    default_peer.monitor.onProcess(['period', 'a'])
    assert default_peer.monitor.loopDelay == origin
    default_peer.monitor.onProcess(['period', '111'])
    assert default_peer.monitor.loopDelay == 111
    default_peer.monitor.onProcess(['period', str(origin)])


def test_verboseCmd(default_peer):
    assert default_peer.monitor.verbose is False
    default_peer.monitor.onProcess(['verbose'])
    assert default_peer.monitor.verbose is True
    default_peer.monitor.onProcess(['verbose'])
    assert default_peer.monitor.verbose is False
