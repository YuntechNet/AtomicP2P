import pytest


def test_init(thread):
    assert thread.loopDelay == 1
    assert thread.stopped.is_set() is False


def test_select_handler(thread):
    assert thread.select_handler(pkt_type="not_exists") is None
    assert thread.select_handler(pkt_type="select_handler") is not None


def test_register_handler(thread, handler):
    assert thread.register_handler(handler=handler) is True
    assert thread.register_handler(handler=handler) is False
    assert thread.register_handler(handler=handler, force=True) is True


def test_unregister_handler(thread, handler):
    thread.register_handler(handler=handler)
    assert thread.unregister_handler(pkt_type="not_exists") is False
    assert thread.unregister_handler(pkt_type=type(handler).pkt_type) is True


def test__register_andler(thread):
    with pytest.raises(NotImplementedError):
        thread._register_handler()


def test_register_command(thread, command):
    assert thread.register_command(command=command) is True
    assert thread.register_command(command=command) is False
    assert thread.register_command(command=command, force=True) is True    


def test_unregister_command(thread, command):
    thread.register_command(command=command)
    assert thread.unregister_command(cmd="not_exists") is False
    assert thread.unregister_command(cmd=command.cmd) is True


def test__register_command(thread):
    with pytest.raises(NotImplementedError):
        thread._register_command()


def test_start(thread):
    thread.start()


def test_stop(thread):
    thread.stop()
    assert thread.stopped.is_set()
