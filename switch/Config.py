import re

from commands.Show import Show

class Interface:
    
    def __init__(self, data):
        self.data = data
        self.name = re.compile('\\r\\ninterface .*?\\r\\n', re.DOTALL).search(self.data).group(0)[12:-2]

class Neighbor:

    def __init__(self, data):
        self.data = data
        self.device = re.compile('\\r\\nDevice ID: .*?\\r\\n', re.DOTALL).search(self.data).group(0)[13:-2]
        self.entryAddrs = self.loadEntryAddress()
        self.platform = re.compile('\\r\\nPlatform: .*?,', re.DOTALL).search(self.data).group(0)[12:-1]
        self.capability = re.compile('Capabilities: .*?\\r\\n', re.DOTALL).search(self.data).group(0)[14:-2]
        self.version = re.compile('Version :\\r\\n.*?\\r\\nCopyright', re.DOTALL).search(self.data).group(0)[11:-11]
        self.manageAddrs = self.loadManageAddress()

    def loadEntryAddress(self):
        entrys = []
        section = re.compile('\\r\\nEntry address\(es\): \\r\\n.*?\\r\\nPlatform', re.DOTALL).search(self.data).group(0)
        for each in re.compile('  IP address: .*?\\r\\n', re.DOTALL).findall(section):
            entrys.append(each[14:-2])
        return entrys

    def loadManageAddress(self):
        manages = []
        section = re.compile('\\r\\nManagement address\(es\): \\r\\n.*?\\r\\n\\x08', re.DOTALL).search(self.data).group(0)
        for each in re.compile('  IP address: .*?\\r\\n', re.DOTALL).findall(section):
            manages.append(each[14:-2])
        return manages

class SwitchConfig:

    def __init__(self, switch):
        self.switch = switch
        
    def loadConfig(self, debug=False):
        showRunStr = self.switch.singleExecute('system', Show('run'), False)
        (self.hostname, showRunStr) = self.__getHostname(showRunStr, debug)
        (self.interfaces, showRunStr) = self.__getInterface(showRunStr, debug)

    def loadNeighbor(self, debug=False):
        showCDPStr = self.switch.singleExecute('system', Show('cdp neighbor detail'), False)
        (self.neighbors, showCDPStr) = self.__getNeighbor(showCDPStr, False)

    def info(self):
        return { 'hostname': self.hostname, 'interfaces': self.interfaces, 'neighbors': self.neighbors }

    def __getHostname(self, string, debug=False):
        section = re.compile('!\\r\\nhostname .*\\r\\n!').search(string).group(0)
        hostname = section[12:-3]
        if debug:
            print(hostname)
        return (hostname, string.replace(section, '!'))
    
    def __getInterface(self, string, debug=False):
        interfaces = []
        section =  re.compile('!\\r\\n!\\r\\n!\\r\\ninterface .*\\r\\n!\\r\\n!\\r\\n!', re.DOTALL).search(string).group(0)
        process = section.replace('!', '!\r\n!')
        for each in re.compile('!\\r\\ninterface .*?\\r\\n!', re.DOTALL).findall(process):
            interfaces.append(Interface(each))
            if debug:
                print(each)
        return (interfaces, string.replace(section, '!\r\n!\r\n!'))

    def __getNeighbor(self, string, debug=False):
        neighbors = []
        for each in re.compile('\\n-------------------------', re.DOTALL).split(string):
            if not 'Device ID' in each:
                continue
            else:
                neighbors.append(Neighbor(each))
                if debug:
                    print(each)
        return (neighbors, '')

