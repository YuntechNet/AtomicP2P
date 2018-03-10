import re

class Interface:
    
    def __init__(self, data):
        self.data = data
        self.loadInterface()

    def loadInterface(self):
        self.name = re.compile('\\r\\ninterface .*?\\r\\n', re.DOTALL).search(self.data).group(0)[12:-2]

class SwitchConfig:

    def __init__(self, switch):
        self.switch = switch
        
    def loadConfig(self, string, debug=False):
        (self.hostname, string) = self.__getHostname(string, debug)
        (self.interface, string) = self.__getInterface(string, debug)

    def __getHostname(self, string, debug=False):
        section = re.compile('!\\r\\nhostname .*\\r\\n!').search(string).group(0)
        hostname = section[12:-3]
        if debug:
            print(hostname)
        return (hostname, string.replace(section, '!'))
    
    def __getInterface(self, string, debug=False):
        interface = []
        section =  re.compile('!\\r\\n!\\r\\n!\\r\\ninterface .*\\r\\n!\\r\\n!\\r\\n!', re.DOTALL).search(string).group(0)
        process = section.replace('!', '!\r\n!')
        for each in re.compile('!\\r\\ninterface .*?\\r\\n!', re.DOTALL).findall(process):
            interface.append(Interface(each))
        if debug:
            print(interface)
        return (interface, string.replace(section, '!\r\n!\r\n!'))
