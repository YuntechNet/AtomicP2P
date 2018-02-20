import re
from commands.Show import Show

class Interface:
    
    def __init__(self, data):
        self.data = data
        self.loadInterface()

    def loadInterface(self):
        self.name = re.compile('\\r\\ninterface .*?\\r\\n', re.DOTALL).search(self.data).group(0)[12:-2]

class SwitchConfig:

    def __init__(self, switch):
        self.switch = switch
        self.loadConfig()
        
    def loadConfig(self, debug=False):
        self.switch.sshClient.login()
        self.switch.executor._mode_()
        (self.switch.executor, result) = self.switch.executor._execute_(Show('run'), short=False)
        result = self.__getHostname(result)
        result = self.__getInterface(result)

        if debug:
            print(result)
        self.switch.sshClient.logout()

    def __getHostname(self, string):
        section = re.compile('!\\r\\nhostname .*\\r\\n!').search(string).group(0)
        self.hostname = section[12:-3]
        return string.replace(section, '!')
    
    def __getInterface(self, string):
        self.interface = []
        section =  re.compile('!\\r\\n!\\r\\n!\\r\\ninterface .*\\r\\n!\\r\\n!\\r\\n!', re.DOTALL).search(string).group(0)
        process = section.replace('!', '!\r\n!')
        for each in re.compile('!\\r\\ninterface .*?\\r\\n!', re.DOTALL).findall(process):
            self.interface.append(Interface(each))
        return string.replace(section, '!\r\n!\r\n!')
