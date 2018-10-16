
class PeerInfo(object):

    def __init__(self, name, role, host):
        self.name = name
        self.role = role
        self.host = host

    def __eq__(self, other):
        return self.name == other.name \
               and self.role == other.role \
               and self.host == other.host \

    def __str__(self):
        return 'PeerInfo<name={0}, role={1}, host={2}>'.format(self.name, self.role, str(self.host))

