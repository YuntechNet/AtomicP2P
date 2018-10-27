import time
from enum import Enum


class StatusType(Enum):
    PENDING = 'pending'
    UPDATED = 'updated'
    NO_RESP = 'no_resp'
    UNKNOWN = 'unknown'


class PeerStatus(object):

    def __init__(self, peer_info, status=StatusType.PENDING):
        self.peer_info = peer_info
        self.last_update_ts = time.time()
        self.no_response_count = 0
        self.status = status

    def __eq__(self, other):
        return self.peer_info == other.peer_info

    def __str__(self):
        return 'PeerStatus<host={}, status={}>'.format(
                    str(self.peer_info.host), self.status)

    def toDict(self):
        return {
            'send_ts': self.last_update_ts
        }

    def update(self, status_type=StatusType.UPDATED):
        if status_type == StatusType.PENDING:
            self.no_response_count += 1
        elif status_type == StatusType.UPDATED:
            self.no_response_count = 0
            self.last_update_ts = time.time()
        self.status = status_type
