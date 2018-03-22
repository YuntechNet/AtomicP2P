from commands.Show import Show

class TestShow:

    def test_init(self):
        command = Show()
        assert command.name == 'show'
        assert command.args == None
