import json

from LibreCisco.utils import printText
from LibreCisco.utils.communication.packet import Packet


class Handler(object):

    def __init__(self, pkt_type, peer, can_broadcast=False):
        self.pkt_type = pkt_type
        self.peer = peer
        self.can_broadcast = can_broadcast

    # Wrap if it is a broadcast packet.
    def wrap_packet(self, message, **kwargs):
        arr = []
        if self.can_broadcast and message.is_broadcast():
            role = message._to[1]
            for each in self.peer.connectlist:
                if role == 'all' or each.role == role:
                    message._to = each.host
                    arr.append(message.copy())
        else:
            arr.append(message)
        return arr

    def onSend(self, target, **kwargs):
        if 'reject_reason' in locals()['kwargs']:
            message = self.onSendReject(target=target, **kwargs)
            return message if type(message) is list else [message]
        else:
            message = self.onSendPkt(target=target, **kwargs)
            return self.wrap_packet(message=message, **kwargs)

    def onSendReject(self, target, reject_reason, **kwargs):
        message = Packet(dst=target, src=self.peer.peer_info.host, _hash=None,
                         _type=self.pkt_type, _data={})
        message.set_reject(reject_reason)
        return message

    def onSendPkt(self, target, **kwargs):
        raise NotImplementedError

    def onRecv(self, src, pkt, **kwargs):
        if pkt.is_reject():
            self.onRecvReject(src=src, pkt=pkt, **kwargs)
        else:
            self.onRecvPkt(src=src, pkt=pkt, **kwargs)

    def onRecvReject(self, src, pkt, conn, **kwargs):
        reject = pkt._data['reject']
        printText('Rejected by {}, reason: {}'.format(pkt._from, reject))
        # TODO: Fit unittest empty conn in PeerInfo
        #       Waiting for use mock.
        #                      - 2019/04/13
        if conn is not None:
            conn.stop()

    def onRecvPkt(self, src, pkt, **kwargs):
        raise NotImplementedError
