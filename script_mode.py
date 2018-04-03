from ssh_switch import ssh_switch
from switch.Switch import Switch
import re
import json

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

class FormatExplainer(ScriptExplainer):

    def __init__(self,script):
        
        self.script = open(script)
        self.commandList = []
        self.preCommand = []
        self.command = []

    def dataLoad(self,data):
        self.data = data
        for each in data:
            self.preCommand.append('%s = %s'%(each,data[each]))

    def parseScript(self):
        varPattern = '{{[^{]+}}'
        blockPattern = '{%.*%}'
        commentPattern = '{#.*#}'
        parseTemp = []
        for line in self.script:
            line = line.strip('\n')
            varList = re.findall(varPattern,line)
            block = re.findall(blockPattern,line) 
            if varList:
                line = "'%s'" % line
                line = self.ParseVariable(line,varList)
                #self.command.append('sw_exec(%s)\n'%line)
            elif block:
                pass
            else:
                line = "'%s'" % line
            parseTemp.append(line)
        self.ParseBlock(parseTemp)
        for each in self.command:
            print(each)

    def ParseBlock(self,parseTemp):
        blockPattern = '{%.*%}'
        flag =False
        blockList = []
        for each in parseTemp:
            if re.search(blockPattern,each): 
                flag = not flag
            if flag:
                blockList.append(each)

        print(blockList)


    def ParseVariable(self,line,varList):

        if len(varList) == 1:
            line = line.replace(varList[0],"%s")
            line = "%s %%(%s)"%(line,varList[0].replace('{','').replace('}',''))
        else:
            for each in varList:
                line = line.replace(each,"%s")
                var = each.replace('{','').replace('}','')
                if re.search(r".*\..*",var): #need improve
                    var = '%s[%s]'%(var.split('.')[0],var.split('.')[1])

                if each == varList[0]:
                    line = "%s %% (%s," %(line,var)
                elif each == varList[-1]:
                    line = "%s %s)" % (line,var)
                else:
                    line = "%s %s,"%(line,var)
         
        return line

    def explainToList(self):
        resultDict = self.scriptPreExec(self.preCommand)
        self.commandList = self._explain_(self.command, resultDict)
        return self.commandList

