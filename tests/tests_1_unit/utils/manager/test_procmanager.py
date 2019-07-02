import pytest

from atomic_p2p.utils.manager import ProcManager


def test_init(proc):
    assert proc.loopDelay == 1
    assert proc.stopped.is_set() is False

def test_select_handler(proc):
    assert proc.select_handler(pkt_type="not_exists") is None
    assert proc.select_handler(pkt_type="select_handler") is not None


def test_register_handler(proc, handler):
    assert proc.register_handler(handler=handler) is True
    assert proc.register_handler(handler=handler) is False
    assert proc.register_handler(handler=handler, force=True) is True


def test_unregister_handler(proc, handler):
    proc.register_handler(handler=handler)
    assert proc.unregister_handler(pkt_type="not_exists") is False
    assert proc.unregister_handler(pkt_type=type(handler).pkt_type) is True


def test__register_handler(proc):
    with pytest.raises(NotImplementedError):
        proc._register_handler()


def test_register_command(proc, command):
    assert proc.register_command(command=command) is True
    assert proc.register_command(command=command) is False
    assert proc.register_command(command=command, force=True) is True    


def test_unregister_command(proc, command):
    proc.register_command(command=command)
    assert proc.unregister_command(cmd="not_exists") is False
    assert proc.unregister_command(cmd=command.cmd) is True


def test__register_command(proc):
    with pytest.raises(NotImplementedError):
        proc._register_command()


def test_start(proc):
    proc.start()


def test_stop(proc):
    proc.stop()
    assert proc.stopped.is_set()


def test_is_start(proc):
    proc.start()
    assert proc.is_start() is True
