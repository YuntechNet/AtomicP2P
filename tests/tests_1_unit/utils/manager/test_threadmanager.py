import pytest


def test_init(thread):
    assert thread.output_field is None
    assert thread.loopDelay == 1
    assert thread.stopped.is_set() is False


def test__register_andler(thread):
    with pytest.raises(NotImplementedError):
        thread._register_handler()


def test__register_command(thread):
    with pytest.raises(NotImplementedError):
        thread._register_command()


def test_start(thread):
    thread.start()


def test_stop(thread):
    thread.stop()
    assert thread.stopped.is_set()
