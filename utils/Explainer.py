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
class Explainer:

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

    def __init__(self, scriptFileName):
        self.scriptFileName = scriptFileName
        scriptFile = open(self.scriptFileName)
        self.script = json.loads(scriptFile.read())
        scriptFile.close()
        self.commandList = []

    def scriptPreExec(self, preCommandCode):
        for each in preCommandCode:
            exec(each, globals(), locals())
        return locals()

    def scriptExplainer(self, commandCode, local):

        def sw_exec(command):
            self.commandList.append(command)

        execCode = ''    
        for each in commandCode:
            execCode += each

        exec(execCode, local, locals())
        return self.commandList

    def explainToList(self):
        resultDict = self.scriptPreExec(self.script['pre_command'])
        self.commandList = self.scriptExplainer(self.script['command'], resultDict)
        return self.commandList
        

