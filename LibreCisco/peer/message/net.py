from LibreCisco.utils import printText
from LibreCisco.utils.message import Message, Handler
from LibreCisco.peer.peer_info import PeerInfo


class JoinHandler(Handler):

    def __init__(self, peer):
        super(JoinHandler, self).__init__(peer, can_reject=True)
        self.output_field = peer.output_field
        self.last_join_host = None

    def onSendPkt(self, target, **kwargs):
        printText('Joining net to:{}'.format(str(target)))
        data = {
           'name': self.peer.peer_info.name,
           'listen_port': int(self.peer.peer_info.host[1]),
           'role': self.peer.peer_info.role
        }
        return Message(_to=target, _from=self.peer.peer_info.host,
                       _hash=self.peer._hash, _type='join', _data=data)

    def onSendReject(self, target, reason, **kwargs):
        message = Message(_to=target, _from=self.peer.peer_info.host,
                          _hash=None, _type='join', _data={})
        message.set_reject(reason)
        return message

    def onRecvPkt(self, src, data, **kwargs):
        name = data['name']
        listen_port = int(data['listen_port'])
        role = data['role']
        peer_info = PeerInfo(name=name, role=role, host=(src[0], listen_port))
        self.last_join_host = peer_info.host
        send_data = {'peer_info': peer_info}
        for each in self.peer.connectlist:
            self.peer.sendMessage((each.host[0], each.host[1]),
                                  'newmember', **send_data)
        printText('Recieve new peer add request: {}, added.'.format(
                    str(peer_info)))
        self.peer.addConnectlist(peer_info)
        self.peer.sendMessage((src[0], listen_port), 'checkjoin')

    def onRecvReject(self, src, data, **kwargs):
        reject = data['reject']
        printText('Rejected by {}, reason: {}'.format(src, reject))


class CheckJoinHandler(Handler):

    def __init__(self, peer):
        super(CheckJoinHandler, self).__init__(peer)
        self.output_field = peer.output_field

    def onSendPkt(self, target, **kwargs):
        data = {
            'name': self.peer.peer_info.name,
            'listen_port': int(self.peer.peer_info.host[1]),
            'role': self.peer.peer_info.role
        }
        return Message(_to=target, _from=self.peer.peer_info.host,
                       _hash=self.peer._hash, _type='checkjoin', _data=data)

    def onRecvPkt(self, src, data):
        name = data['name']
        listen_port = int(data['listen_port'])
        role = data['role']
        peer_info = PeerInfo(name=name, role=role, host=(src[0], listen_port))
        printText('Added peer:' + str(peer_info))
        self.peer.addConnectlist(peer_info)


class NewMemberHandler(Handler):

    def __init__(self, peer):
        super(NewMemberHandler, self).__init__(peer)
        self.output_field = peer.output_field

    def onSendPkt(self, target, peer_info, **kwargs):
        data = {
            'name': peer_info.name,
            'listen_port': int(peer_info.host[1]),
            'role': peer_info.role
        }
        return Message(_to=target, _from=self.peer.peer_info.host,
                       _hash=self.peer._hash, _type='newmember', _data=data)

    def onRecvPkt(self, src, data):
        name = data['name']
        listen_port = int(data['listen_port'])
        role = data['role']
        peer_info = PeerInfo(name=name, role=role, host=(src[0], listen_port))
        printText('New peer join net:' + str(peer_info))
        self.peer.addConnectlist(peer_info)
        self.peer.sendMessage((src[0], listen_port), 'checkjoin')
