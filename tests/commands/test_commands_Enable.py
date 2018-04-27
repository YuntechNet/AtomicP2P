from utils.Executor import Executor
from utils.Enums import SwitchMode
from commands.Enable import Enable

class TestEnable:

    def test_init(self):
        command = Enable()
        assert command.name == 'enable'

    def test_preExecute(self):
        exe = Executor()
        exe.mode = SwitchMode.DEFAULT
        command = Enable()
        command.__pre_execute__(exe)
        assert exe.mode == SwitchMode.ENABLE
