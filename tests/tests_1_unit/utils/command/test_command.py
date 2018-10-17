import pytest
from LibreCisco.utils.command import Command


def test_init(command):
    assert command.cmd is None


def test_onProcess(command):
    with pytest.raises(NotImplementedError):
        command.onProcess(None)
