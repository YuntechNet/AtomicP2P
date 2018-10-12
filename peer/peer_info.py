
class PeerInfo(object):

    def __init__(self, name, role, host):
        self.name = name
        self.role = role
        self.host = host

    def __contains__(self, value):
        return value.host == self.host or value.name == self.name

    def __str__(self):
        return 'PeerInfo<name={0}, role={1}, host={2}>'.format(self.name, self.role, str(self.host))

