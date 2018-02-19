from commands.Command import Command
from enums.SwitchMode import SwitchMode

class Exit(Command):

    reg = '^(exit)'
    mode = SwitchMode.EN_CONF

    def __init__(self):
        super().__init__()
        self.name = 'exit'

    def __pre_execute__(self, exe):
        if exe.mode == SwitchMode.CONTER:
           exe.mode = SwitchMode.ENABLE
        elif exe.mode == SwitchMode.ENABLE:
           exe.mode = SwitchMode.DEFAULT
        else:
           pass
