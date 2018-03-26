import pytest

from commands.Command import Command

class TestCommand:

    def test_init(self):
        c = Command()
        assert c.name == ''
        assert c.args == ''

    def test_insert(self):
        c = Command()
        c._insert_(' args')
        assert c.args == 'args'

    @pytest.mark.skip('L18-35:Need switch for unit test')
    def test_execute(self):
        pass

    def test_preExecute(self):
        c = Command()
        c.__pre_execute__(None)

    def test_postExecute(self):
        c = Command()
        c.__post_execute__(None)
