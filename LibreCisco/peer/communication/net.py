from time import sleep

from LibreCisco.utils import printText
from LibreCisco.peer.entity.peer_info import PeerInfo
from LibreCisco.utils.communication import Packet, Handler


class JoinHandler(Handler):
    pkt_type = 'peer-join'

    def __init__(self, peer):
        super(JoinHandler, self).__init__(pkt_type=type(self).pkt_type,
                                          peer=peer)
        self.output_field = peer.output_field
        self.last_join_host = None

    def on_send_pkt(self, target):
        printText('Joining net to:{}'.format(str(target)))
        data = {
           'name': self.peer.server_info.name,
           'listen_port': int(self.peer.server_info.host[1]),
           'role': self.peer.server_info.role
        }
        return Packet(dst=target, src=self.peer.server_info.host,
                      _hash=self.peer._hash, _type=type(self).pkt_type,
                      _data=data)

    def on_recv_pkt(self, src, pkt, conn):
        data = pkt.data
        name = data['name']
        listen_port = int(data['listen_port'])
        role = data['role']
        peer_info = PeerInfo(name=name, role=role, host=(src[0], listen_port),
                             conn=conn)

        handler = self.peer.select_handler(pkt_type=NewMemberHandler.pkt_type)
        for (key, value) in self.peer.peer_pool.items():
            pkt = handler.on_send_pkt(target=key, **{'peer_info': peer_info})
            self.peer.pend_packet(pkt=pkt, sock=value.conn)
        printText('Recieve new peer add request: {}, added.'.format(
                    str(peer_info)))

        handler = self.peer.select_handler(pkt_type=CheckJoinHandler.pkt_type)
        pkt = handler.on_send_pkt(target=(src[0], listen_port))
        self.peer.pend_socket(sock=conn)
        self.peer.pend_packet(pkt=pkt, sock=conn)
        self.peer.add_peer_in_net(peer_info=peer_info)


class CheckJoinHandler(Handler):
    pkt_type = 'peer-checkjoin'

    def __init__(self, peer):
        super(CheckJoinHandler, self).__init__(pkt_type=type(self).pkt_type,
                                               peer=peer)
        self.output_field = peer.output_field

    def on_send_pkt(self, target):
        data = {
            'name': self.peer.server_info.name,
            'listen_port': int(self.peer.server_info.host[1]),
            'role': self.peer.server_info.role
        }
        return Packet(dst=target, src=self.peer.server_info.host,
                      _hash=self.peer._hash, _type=type(self).pkt_type,
                      _data=data)

    def on_recv_pkt(self, src, pkt, conn):
        data = pkt.data
        name = data['name']
        listen_port = int(data['listen_port'])
        role = data['role']
        peer_info = PeerInfo(name=name, role=role, host=(src[0], listen_port),
                             conn=conn)
        printText('Added peer:' + str(peer_info))
        self.peer.add_peer_in_net(peer_info=peer_info)


class NewMemberHandler(Handler):
    pkt_type = 'peer-new-member'

    def __init__(self, peer):
        super(NewMemberHandler, self).__init__(pkt_type=type(self).pkt_type,
                                               peer=peer)
        self.output_field = peer.output_field

    def on_send_pkt(self, target, peer_info):
        data = {
            'name': peer_info.name,
            'addr': peer_info.host[0],
            'listen_port': int(peer_info.host[1]),
            'role': peer_info.role
        }
        return Packet(dst=target, src=self.peer.server_info.host,
                      _hash=self.peer._hash, _type=type(self).pkt_type,
                      _data=data)

    def on_recv_pkt(self, src, pkt, conn):
        data = pkt.data
        name = data['name']
        addr = data['addr']
        listen_port = int(data['listen_port'])
        role = data['role']

        handler = self.peer.select_handler(
                    pkt_type=AckNewMemberHandler.pkt_type)
        pkt = handler.on_send(target=(addr, listen_port))
        sock = self.peer.new_tcp_long_conn(dst=(addr, listen_port))
        peer_info = PeerInfo(
            name=name, role=role, host=(addr, listen_port), conn=sock)
        self.peer.pend_socket(sock=sock)
        self.peer.pend_packet(sock=sock, pkt=pkt)

        printText('New peer join net: {}'.format(peer_info))
        self.peer.add_peer_in_net(peer_info=peer_info)


class AckNewMemberHandler(Handler):
    pkt_type = 'peer-ack-new-memeber'

    def __init__(self, peer):
        super(AckNewMemberHandler, self).__init__(pkt_type=type(self).pkt_type,
                                                  peer=peer)
        self.output_field = peer.output_field

    def on_send_pkt(self, target):
        data = {
            'name': self.peer.server_info.name,
            'role': self.peer.server_info.role,
            'listen_port': int(self.peer.server_info.host[1])
        }
        return Packet(dst=target, src=self.peer.server_info.host,
                      _hash=self.peer._hash, _type=type(self).pkt_type,
                      _data=data)

    def on_recv_pkt(self, src, pkt, conn):
        data = pkt.data
        name = data['name']
        role = data['role']
        listen_port = int(data['listen_port'])
        peer_info = PeerInfo(name=name, role=role, host=(src[0], listen_port),
                             conn=conn)
        self.peer.add_peer_in_net(peer_info=peer_info)
        self.peer.pend_socket(sock=conn)
        printText('ACK new member join net: {}'.format(peer_info))


class DisconnectHandler(Handler):
    pkt_type = 'peer-disconnect'

    def __init__(self, peer):
        super(DisconnectHandler, self).__init__(pkt_type=type(self).pkt_type,
                                                peer=peer)
        self.output_field = peer.output_field

    def on_send_pkt(self, target):
        return Packet(dst=target, src=self.peer.server_info.host,
                      _hash=self.peer._hash, _type=type(self).pkt_type,
                      _data={})

    def on_recv_pkt(self, src, pkt, conn):
        peer_info = self.peer.peer_pool[pkt.src]
        self.peer.del_peer_in_net(peer_info=peer_info)
        self.peer.pend_socket_to_rm(sock=conn)
        printText('Received Stop Signal from {} and Stopped.'.format(pkt.src))
