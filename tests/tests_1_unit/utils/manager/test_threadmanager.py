import pytest


def test_init(thread):
    assert thread.loopDelay == 1
    assert thread.stopped.is_set() is False


def test_registerHandler(thread):
    with pytest.raises(NotImplementedError):
        thread.registerHandler()


def test_registerCommand(thread):
    with pytest.raises(NotImplementedError):
        thread.registerCommand()


def test_start(thread):
    thread.start()


def test_stop(thread):
    thread.stop()
    assert thread.stopped.is_set()
