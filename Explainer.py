import re
from commands.Enable import Enable
from commands.ConfigTerminal import ConfigTerminal
from commands.Show import Show
from commands.Exit import Exit

class Explainer:

    commands = [
        Enable(), ConfigTerminal(), Show(), Exit()
    ]

    def __init__(self):
        pass

    def _explain_(self, cmd):
        for each in self.commands:
            if re.compile(each.reg).match(cmd):
                return each
        return None
