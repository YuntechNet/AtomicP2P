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

    def onSendPkt(self, target, status):
        data = status.toDict()
        return Message(_to=target, _from=self.peer.peer_info.host,
                       _hash=self.peer._hash, _type=self.pkt_type, _data=data)

    def onRecvPkt(self, src, data):
        message = 'WatchDog check from {}: send ts {}'.format(str(src),
                                                              data['send_ts'])
        if self.watchdog.verbose:
            printText(message)

    def onRecvReject(self, src, data):
        if self.watchdog.verbose:
            super(CheckHandler, self).onRecvReject(src, data)
        status, peer_info = self.watchdog.getStatusByHost(src)
        if status:
            status.update(status_type=StatusType.PENDING)
