from typing import Dict
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
        last_update_ts (float): Last update timestamp.
        no_response_count (int): No response count since last check.
        status (StatusType): Current peer status.
    """

    def __init__(self, status: 'StatusType' = StatusType.PENDING) -> None:
        """Init of PeerStatus

        Args:
            status: Peer status, default is StatusType.PENDING when init.
        """
        self.last_update_ts = time.time()
        self.no_response_count = 0
        self.status = status

    def __str__(self):
        return str(self.status)

    def toDict(self) -> Dict:
        return {
            'send_ts': self.last_update_ts
        }

    def update(self, status_type: 'StatusType' = StatusType.UPDATED) -> None:
        if status_type == StatusType.PENDING:
            self.no_response_count += 1
        elif status_type == StatusType.UPDATED:
            self.no_response_count = 0
            self.last_update_ts = time.time()
        self.status = status_type
