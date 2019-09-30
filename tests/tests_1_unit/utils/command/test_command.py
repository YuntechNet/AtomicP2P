from pytest import raises

from atomic_p2p.communication.command import Command


def test_init(command):
    assert command.cmd is None


def test__execute(command):
    with raises(NotImplementedError):
        command._execute(None)
