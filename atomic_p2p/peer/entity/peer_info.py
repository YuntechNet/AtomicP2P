from atomic_p2p.peer.entity.peer_status import PeerStatus, StatusType


class PeerInfo(object):

    def __init__(self, name, role, host, status=StatusType.PENDING, conn=None):
        self.name = name
        self.role = role
        self.host = (host[0], int(host[1]))
        self.status = PeerStatus(status=status)
        self.conn = conn

    def __eq__(self, other):
        return other is not None and self.name == other.name and \
               self.role == other.role and self.host == other.host

    def __contains__(self, item):
        return self.__eq__(item)

    def __str__(self):
        return 'PeerInfo<name={0}, role={1}, host={2}>'.format(self.name,
                                                               self.role,
                                                               str(self.host))
