from peer.message import Message, Handler

class MessageHandler(Handler):

    def __init__(self, peer):
        super(MessageHandler, self).__init__(peer)

    def onSend(self, target, msg, **kwargs):
        data = {
            'message': msg
        }
        return Message(_ip=target, _type='message', _data=data)

    def onRecv(self, src, data):
        message = data['message']
        print('Message from {}: {}'.format(str(src), message))

class BroadcastHandler(Handler):

    def __init__(self, peer):
        super(BroadcastHandler, self).__init__(peer)

    def onSend(self, target, role, msg, **kwargs):
        data = {
            'from_name': self.peer.name,
            'role': role,
            'msg': msg
        }
        return Message(_ip=target, _type='broadcast', _data=data)

    def onRecv(self, src, data):
        from_name = data['from_name']
        role = data['role']
        msg = data['msg']
        if self.peer.role == role or 'all' == role:
            print('Broadcast Mmessage from: {}: {}'.format(from_name, msg))
