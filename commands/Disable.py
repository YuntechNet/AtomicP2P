from commands.Command import Command
from utils.Enums import SwitchMode

class Disable(Command):

    reg = '^(disa){1}(ble)?'
    mode = SwitchMode.ENABLE

    def __init__(self):
        super().__init__()
        self.name = 'disable'

    def __execute__(self, exe):
        if exe.mode == SwitchMode.ENABLE:
            exe.mode = SwitchMode.DEFAULT
        else:
            pass
