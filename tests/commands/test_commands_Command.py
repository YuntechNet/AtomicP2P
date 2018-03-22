import pytest

from commands.Command import Command

class TestCommand:

    def test_init(self):
        command = Command()
        assert command.name == ''
        assert command.args == ''

    def test_insert(self):
        command = Command()
        command._insert_(' args')
        assert command.args == 'args'

    @pytest.mark.skip(reason="Need switch for unit test")
    def test_execute(self):
        command = Command()

    def test_preExecute(self):
        pass

    def test_postExecute(self):
        pass
