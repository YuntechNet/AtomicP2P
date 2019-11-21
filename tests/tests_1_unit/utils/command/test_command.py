from pytest import raises


def test_init(command):
    assert command.cmd is None


def test__execute(command):
    with raises(NotImplementedError):
        command._execute(None)
