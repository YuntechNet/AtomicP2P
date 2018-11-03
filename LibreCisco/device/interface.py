import re


class Interface(object):

    def fromReString(re_str):
        name = re_str[:re_str.index(' ')]
        return Interface(name=name)

    def fromString(string):
        interfaces = []
        for each in string.split('\n'):
            if 'connected' in each or 'notconnect' in each:
                interfaces.append(Interface.fromReString(re_str=each))
        return interfaces

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Interface<name={}>'.format(self.name)
