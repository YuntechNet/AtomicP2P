import time


class PeerStatus(object):

    def __init__(self, peer_info):
        self.peer_info = peer_info
        self.last_update_ts = time.time()
        self.no_response_count = 0

    def __eq__(self, other):
        return self.peer_info == other.peer_info

    def __str__(self):
        return 'PeerStatus<host={}>'.format(str(self.peer_info.host))

    def toDict(self):
        return {
            'send_ts': self.last_update_ts
        }

    def update(self):
        self.last_update_ts = time.time()
