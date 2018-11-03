import re


class DeviceInfo(object):

    @staticmethod
    def fromString(string):
        print(string)
        version = re.search('version .*?\n', string).group(0)[8:-2]
        hostname = re.search('hostname .*?\n', string).group(0)[9:-2]
        return DeviceInfo(version=version, hostname=hostname)

    def __init__(self, version, hostname):
        self.version = version
        self.hostname = hostname

    def __str__(self):
        return 'DeviceInfo<version={}, hostname={}>'.format(self.version,
                                                            self.hostname)
