from commands.Command import Command
from enums.SwitchMode import SwitchMode

class ConfigTerminal(Command):
    
    reg = '^conf{1}(igure)? {1}ter{1}(minal)?'

    def __init__(self):
        super().__init__()
        self.name = 'configure terminal'

    def __execute__(self, exe):
        if exe.mode == SwitchMode.ENABLE:
            exe.mode = SwitchMode.CONFTER
        else:
            pass
