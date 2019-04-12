from LibreCisco.utils import printText
from LibreCisco.utils.communication import Message, Handler


class MessageHandler(Handler):
    pkt_type = 'message'

    def __init__(self, peer):
        super(MessageHandler, self).__init__(pkt_type=type(self).pkt_type,
                                             peer=peer, can_broadcast=True)
        self.output_field = peer.output_field

    def onSendPkt(self, target, msg):
        data = {
            'message': msg
        }
        return Message(_to=target, _from=self.peer.peer_info.host,
                       _hash=self.peer._hash, _type=type(self).pkt_type,
                       _data=data)

    def onRecvPkt(self, src, pkt, conn):
        data = pkt._data
        message = 'Message from {}: {}'.format(str(src), data['message'])
        self.peer.last_output = message
        printText(message)
