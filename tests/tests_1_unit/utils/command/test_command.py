import pytest
from atomic_p2p.utils.command import Command


def test_init(command):
    assert command.cmd is None


def test_onProcess(command):
    with pytest.raises(NotImplementedError):
        command.onProcess(None)
