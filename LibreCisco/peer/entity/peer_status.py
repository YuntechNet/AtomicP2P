import time
from enum import Enum


class StatusType(Enum):
    PENDING = 'pending'
    UPDATED = 'updated'
    NO_RESP = 'no_resp'
    UNKNOWN = 'unknown'


class PeerStatus(object):
    """Handling status of a PeerInfo
    This class is responsible to handling all detail when Monitor class is in-
    teracting with PeerInfo during packet delivering. Including last update
    time, no response count and etc.

    Attributes:
        last_update_ts: A float stores last update timestamp.
        no_response_count: A integer counter stores no response count since la-
                           st check.
        status: A StatusType represents current peer status.
    """

    def __init__(self, status=StatusType.PENDING):
        """Init of PeerStatus
        Args:
            status: A StatusType to be init, default is StatusType.PENDING.
        """
        self.last_update_ts = time.time()
        self.no_response_count = 0
        self.status = status

    def __str__(self):
        return str(self.status)

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
