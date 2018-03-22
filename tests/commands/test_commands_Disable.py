from utils.Executor import Executor
from utils.Enums import SwitchMode
from commands.Disable import Disable

class TestDisable:

    def test_init(self):
        command = Disable()
        assert command.name == 'disable'

    def test_execute(self):
        exe = Executor()
        exe.mode = SwitchMode.ENABLE
        command = Disable()
        command.__execute__(exe)
        assert exe.mode == SwitchMode.DEFAULT
