from utils.Executor import Executor
from utils.Enums import SwitchMode
from commands.Exit import Exit

class TestExit:

    def test_init(self):
        command = Exit()
        assert command.name == 'exit'

    def test_preExecute(self):
        exe = Executor()
        exe.mode = SwitchMode.CONTER
        command = Exit()
        command.__pre_execute__(exe)
        assert exe.mode == SwitchMode.ENABLE
        command.__pre_execute__(exe)
        assert exe.mode == SwitchMode.DEFAULT

