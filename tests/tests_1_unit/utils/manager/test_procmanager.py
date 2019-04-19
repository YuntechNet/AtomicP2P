import pytest


def test_init(proc):
    assert proc.output_field is None
    assert proc.loopDelay == 1
    assert proc.stopped.is_set() is False


def test__register_handler(proc):
    with pytest.raises(NotImplementedError):
        proc._register_handler()


def test__register_command(proc):
    with pytest.raises(NotImplementedError):
        proc._register_command()


def test_start(proc):
    proc.start()


def test_stop(proc):
    proc.stop()
    assert proc.stopped.is_set()
