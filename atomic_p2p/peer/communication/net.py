from time import sleep

from atomic_p2p.peer.entity.peer_info import PeerInfo
from atomic_p2p.utils.communication import Packet, Handler


class JoinHandler(Handler):
    pkt_type = 'peer-join'

    def __init__(self, peer):
        super(JoinHandler, self).__init__(
            pkt_type=type(self).pkt_type, peer=peer)
        self.last_join_host = None

    def on_send_pkt(self, target):
        self.peer.logger.info('Joining net to:{}'.format(str(target)))
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

        self.peer.handler_broadcast_packet(
            host=('', 'all'), pkt_type=NewMemberHandler.pkt_type,
            **{'peer_info': peer_info})
        self.peer.logger.info('Recieve new peer add request: {}, added.'.format(
                    str(peer_info)))

        self.peer.pend_socket(sock=conn)
        self.peer.add_peer_in_net(peer_info=peer_info)
        self.peer.handler_unicast_packet(
            host=(src[0], listen_port), pkt_type=CheckJoinHandler.pkt_type)


class CheckJoinHandler(Handler):
    pkt_type = 'peer-checkjoin'

    def __init__(self, peer):
        super(CheckJoinHandler, self).__init__(
            pkt_type=type(self).pkt_type, peer=peer)

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
        self.peer.logger.info('Added peer:' + str(peer_info))
        self.peer.add_peer_in_net(peer_info=peer_info)


class NewMemberHandler(Handler):
    pkt_type = 'peer-new-member'

    def __init__(self, peer):
        super(NewMemberHandler, self).__init__(
            pkt_type=type(self).pkt_type, peer=peer)

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

        sock = self.peer.new_tcp_long_conn(dst=(addr, listen_port))
        peer_info = PeerInfo(
            name=name, role=role, host=(addr, listen_port), conn=sock)

        self.peer.pend_socket(sock=sock)
        self.peer.add_peer_in_net(peer_info=peer_info)
        self.peer.handler_unicast_packet(
            host=(addr, listen_port), pkt_type=AckNewMemberHandler.pkt_type)

        self.peer.logger.info('New peer join net: {}'.format(peer_info))


class AckNewMemberHandler(Handler):
    pkt_type = 'peer-ack-new-memeber'

    def __init__(self, peer):
        super(AckNewMemberHandler, self).__init__(
            pkt_type=type(self).pkt_type, peer=peer)

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
        self.peer.logger.info('ACK new member join net: {}'.format(peer_info))


class DisconnectHandler(Handler):
    pkt_type = 'peer-disconnect'

    def __init__(self, peer):
        super(DisconnectHandler, self).__init__(
            pkt_type=type(self).pkt_type, peer=peer)

    def on_send_pkt(self, target):
        return Packet(dst=target, src=self.peer.server_info.host,
                      _hash=self.peer._hash, _type=type(self).pkt_type,
                      _data={})

    def on_recv_pkt(self, src, pkt, conn):
        peer_info = self.peer.get_peer_info_by_host(host=pkt.src)
        if peer_info is not None:
            self.peer.del_peer_in_net(peer_info=peer_info)
            self.peer.pend_socket_to_rm(sock=conn)
            self.peer.logger.info('Received Stop Signal from {}, Stopped.'.format(pkt.src))
