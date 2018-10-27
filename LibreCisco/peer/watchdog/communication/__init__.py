from LibreCisco.utils import printText
from LibreCisco.utils.communication import Message, Handler


class CheckHandler(Handler):

    def __init__(self, watchdog):
        super(CheckHandler, self).__init__(peer=watchdog.peer,
                                           can_reject=False,
                                           can_broadcast=True)
        self.watchdog = watchdog
        self.output_field = self.peer.output_field

    def onSendPkt(self, target, status):
        data = status.toDict()
        return Message(_to=target, _from=self.peer.peer_info.host,
                       _hash=self.peer._hash, _type='watchdog_check',
                       _data=data)

    def onRecvPkt(self, src, data):
        message = 'WatchDog check from {}: send ts {}'.format(str(src),
                                                              data['send_ts'])
        if self.watchdog.verbose:
            printText(message)
