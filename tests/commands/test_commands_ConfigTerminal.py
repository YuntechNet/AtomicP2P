from utils.Executor import Executor
from utils.Enums import SwitchMode
from commands.ConfigTerminal import ConfigTerminal

class TestConfigTerminal:

    def test_init(self):
        command = ConfigTerminal()
        assert command.name == 'configure terminal'

    def test_preExecute(self):
        exe = Executor()
        exe.mode = SwitchMode.ENABLE
        command = ConfigTerminal()
        command.__pre_execute__(exe)
        assert exe.mode == SwitchMode.CONTER
