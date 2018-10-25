from LibreCisco.utils import printText
from LibreCisco.utils.communication import Message, Handler


class CheckHandler(Handler):

    def __init__(self, peer):
        super(CheckHandler, self).__init__(peer=peer, can_reject=False,
                                           can_broadcast=True)
        self.output_field = peer.output_field

    def onSendPkt(self, target, status):
        data = status.toDict()
        return Message(_to=target, _from=self.peer.peer_info.host,
                       _hash=self.peer._hash, _type='watchdog_check',
                       _data=data)

    def onRecvPkt(self, src, data):
        message = 'WatchDog check from {}: send ts {}'.format(str(src),
                                                              data['send_ts'])
        printText(message)
