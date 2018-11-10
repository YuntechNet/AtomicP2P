from LibreCisco.utils.communication import Message, Handler


class MessageHandler(Handler):

    def __init__(self, peer):
        super(MessageHandler, self).__init__(pkt_type='message', peer=peer,
                                             can_broadcast=True)

    def onSendPkt(self, target, msg):
        data = {
            'message': msg
        }
        return Message(_to=target, _from=self.peer.peer_info.host,
                       _hash=self.peer._hash, _type=self.pkt_type, _data=data)

    def onRecvPkt(self, src, pkt):
        data = pkt._data
        message = 'Message from {}: {}'.format(str(src), data['message'])
        self.peer.last_output = message
        self.logger.info(message)
