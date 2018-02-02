from commands.Command import Command
from enums.SwitchMode import SwitchMode

class Disable(Command):

    reg = '^(disa){1}(ble)?'

    def __init__(self):
        super().__init__()
        self.name = 'disable'

    def __execute__(self, exe):
        if exe.mode == SwitchMode.ENABLE:
            exe.mode = SwitchMode.DEFAULT
        else:
            pass
