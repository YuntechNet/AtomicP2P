from commands.Hostname import Hostname

class TestHostname:

    def test_init(self):
        command = Hostname()
        assert command.name == 'hostname'
        assert command.args == None
