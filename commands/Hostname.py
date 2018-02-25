from commands.Command import Command
from enums.SwitchMode import SwitchMode

class Hostname(Command):
    reg = '^(ho){1}(stname)?'
    mode = SwitchMode.CONTER

    def __init__(self,args=None):
        super().__init__()
        self.name = 'hostname'
        self.args = args 