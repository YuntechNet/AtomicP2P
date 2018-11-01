import re


class Interface(object):

    def fromReString(re_str):
        name_str = '\\r\\ninterface .*?\\r\\n'
        name = re.compile(name_str, re.DOTALL).search(re_str).group(0)[12:-2]
        return Interface(name=name)

    def fromString(string):
        interfaces = []
        section_str = '!\\r\\n!\\r\\n!\\r\\ninterface .*\\r\\n!\\r\\n!\\r\\n!'
        section = re.compile(section_str, re.DOTALL).search(string).group(0)
        process = section.replace('!', '!\r\n!')
        separator = '!\\r\\ninterface .*?\\r\\n!'
        for each in re.compile(separator, re.DOTALL).findall(process):
            interfaces.append(Interface.fromReString(re_str=each))
        return interfaces

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Interface<name={}>'.format(self.name)
