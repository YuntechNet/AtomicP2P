from commands.Command import Command
from enums.SwitchMode import SwitchMode

class Enable(Command):

    reg = '^(en){1}(able)?'
    mode = SwitchMode.DEFAULT

    def __init__(self):
        super().__init__()
        self.name = 'enable'

    def __execute__(self, exe):
        if exe.mode == SwitchMode.DEFAULT:
            exe.mode = SwitchMode.ENABLE
        else:
            pass
