from LibreCisco.utils import printText
from LibreCisco.utils.message import Message, Handler


class MessageHandler(Handler):

    def __init__(self, peer):
        super(MessageHandler, self).__init__(peer=peer, can_broadcast=True)
        self.output_field = peer.output_field

    def onSendPkt(self, target, msg, **kwargs):
        data = {
            'message': msg
        }
        return Message(_to=target, _from=self.peer.peer_info.host, _hash=self.peer._hash,
                       _type='message', _data=data)

    def onRecv(self, src, data):
        message = 'Message from {}: {}'.format(str(src), data['message'])
        self.peer.last_output = message
        printText(message)
