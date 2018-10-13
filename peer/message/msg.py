from utils import printText
from utils.message import Message, Handler

class MessageHandler(Handler):

    def __init__(self, peer):
        super(MessageHandler, self).__init__(peer)
        self.output_field = peer.output_field

    def onSend(self, target, msg, **kwargs):
        data = {
            'message': msg
        }
        return Message(_host=target, _type='message', _data=data)

    def onRecv(self, src, data):
        message = 'Message from {}: {}'.format(str(src), data['message'])
        self.peer.last_output = message
        printText(message)

class BroadcastHandler(Handler):

    def __init__(self, peer):
        super(BroadcastHandler, self).__init__(peer)
        self.output_field = peer.output_field

    def onSend(self, target, role, msg, **kwargs):
        data = {
            'from_name': self.peer.name,
            'role': role,
            'msg': msg
        }
        return Message(_host=target, _type='broadcast', _data=data)

    def onRecv(self, src, data):
        from_name = data['from_name']
        role = data['role']
        msg = data['msg']
        if self.peer.role == role or 'all' == role:
            message = 'Broadcast Mmessage from: {}: {}'.format(from_name, msg)
            self.peer.last_output = message
            printText(message)

