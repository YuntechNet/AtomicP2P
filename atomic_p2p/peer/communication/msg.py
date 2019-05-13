from atomic_p2p.utils.communication import Packet, Handler


class MessageHandler(Handler):
    pkt_type = 'message'

    def __init__(self, peer):
        super(MessageHandler, self).__init__(
            pkt_type=type(self).pkt_type, peer=peer)

    def on_send_pkt(self, target, msg):
        data = {
            'message': msg
        }
        return Packet(dst=target, src=self.peer.server_info.host,
                      _hash=self.peer._hash, _type=type(self).pkt_type,
                      _data=data)

    def on_recv_pkt(self, src, pkt, conn):
        data = pkt.data
        message = 'Message from {}: {}'.format(str(src), data['message'])
        self.peer.last_output = message
        self.peer.logger.info(message)
