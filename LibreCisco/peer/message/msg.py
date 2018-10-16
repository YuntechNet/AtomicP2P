from LibreCisco.utils import printText
from LibreCisco.utils.message import Message, Handler


class MessageHandler(Handler):

    def __init__(self, peer):
        super(MessageHandler, self).__init__(peer=peer, can_broadcast=True)
        self.output_field = peer.output_field

    def onSend(self, target, msg, **kwargs):
        data = {
            'message': msg
        }
        return self.wrap_packet(target=target, _type='message', _data=data)

    def onRecv(self, src, data):
        message = 'Message from {}: {}'.format(str(src), data['message'])
        self.peer.last_output = message
        printText(message)
