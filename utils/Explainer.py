import re, json
from commands.Enable import Enable
from commands.Disable import Disable
from commands.ConfigTerminal import ConfigTerminal
from commands.Show import Show
from commands.Exit import Exit
from commands.Hostname import Hostname

# Explainer
#   Class definition of EVERY exists command's explain.
#   Responsible to convert string into specific command's RegEx.
#
class CommandExplainer:

    commands = [
        Hostname(),Enable(), Disable(), ConfigTerminal(), Show(), Exit()
    ]

    def __init__(self):
        pass

    def _explain_(self, cmd):
        for each in self.commands:
            if re.compile(each.reg).match(cmd):
                return each._insert_(cmd)
        return None

class ScriptExplainer:

    def __init__(self, json):
        self.script = json
        self.commandList = []

    def scriptPreExec(self, preCommandCode):
        for each in preCommandCode:
            exec(each, globals(), locals())
        return locals()

    def _explain_(self, commandCode, local):
        def sw_exec(command):
            self.commandList.append(command)

        excCode = ''
        for each in commandCode:
            excCode += each

        exec(excCode, local, locals())
        return self.commandList

    def explainToList(self):
        resultDict = self.scriptPreExec(self.script['preCommand'])
        self.commandList = self._explain_(self.script['command'], resultDict)
        return self.commandList
        
