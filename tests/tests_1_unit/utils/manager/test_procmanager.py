import pytest


def test_init(proc):
    assert proc.output_field is None
    assert proc.loopDelay == 1
    assert proc.stopped.is_set() is False


def test_registerHandler(proc):
    with pytest.raises(NotImplementedError):
        proc.registerHandler()


def test_registerCommand(proc):
    with pytest.raises(NotImplementedError):
        proc.registerCommand()


def test_start(proc):
    proc.start()


def test_stop(proc):
    proc.stop()
    assert proc.stopped.is_set()
