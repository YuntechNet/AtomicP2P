import pytest

from atomic_p2p.utils.manager import ProcManager


def test_init(proc):
    assert proc.loopDelay == 1
    assert proc.stopped.is_set() is False


def test_start(proc):
    proc.start()


def test_stop(proc):
    proc.stop()
    assert proc.stopped.is_set()


def test_is_start(proc):
    proc.start()
    assert proc.is_start() is True
