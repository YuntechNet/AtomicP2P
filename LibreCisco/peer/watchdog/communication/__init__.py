import time
from LibreCisco.peer.watchdog.peer_status import StatusType
from LibreCisco.utils import printText
from LibreCisco.utils.communication import Message, Handler


class CheckHandler(Handler):

    def __init__(self, watchdog):
        super(CheckHandler, self).__init__(pkt_type='watchdog_check',
                                           peer=watchdog.peer,
                                           can_broadcast=True)
        self.watchdog = watchdog
        self.output_field = self.peer.output_field

    def onSendPkt(self, target):
        data = {'send_ts': time.time()}
        return Message(_to=target, _from=self.peer.peer_info.host,
                       _hash=self.peer._hash, _type=self.pkt_type, _data=data)

    def onRecvPkt(self, src, pkt):
        data = pkt._data
        message = 'WatchDog check from {}: send ts {}'.format(pkt._from,
                                                              data['send_ts'])
        if self.watchdog.verbose:
            printText(message)

    def onRecvReject(self, src, pkt):
        if self.watchdog.verbose:
            super(CheckHandler, self).onRecvReject(src, pkt)
        status, peer_info = self.watchdog.getStatusByHost(pkt._from)
        if status:
            status.update(status_type=StatusType.PENDING)
