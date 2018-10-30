import pytest


def test_pauseCmd(default_peer):
    assert default_peer.watchdog.pause is False
    default_peer.watchdog.onProcess(['pause'])
    assert default_peer.watchdog.pause is True
    default_peer.watchdog.onProcess(['pause'])
    assert default_peer.watchdog.pause is False


def test_periodCmd(default_peer):
    origin = default_peer.watchdog.loopDelay
    default_peer.watchdog.onProcess(['period', 'a'])
    assert default_peer.watchdog.loopDelay == origin
    default_peer.watchdog.onProcess(['period', '111'])
    assert default_peer.watchdog.loopDelay == 111
    default_peer.watchdog.onProcess(['period', str(origin)])


def test_verboseCmd(default_peer):
    assert default_peer.watchdog.verbose is False
    default_peer.watchdog.onProcess(['verbose'])
    assert default_peer.watchdog.verbose is True
    default_peer.watchdog.onProcess(['verbose'])
    assert default_peer.watchdog.verbose is False
