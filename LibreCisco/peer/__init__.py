import threading
import socket
import ssl

from threading import Event

from LibreCisco.peer.peer_info import PeerInfo
from LibreCisco.peer.connection import PeerConnection
from LibreCisco.peer.command import SendCmd, ListCmd
from LibreCisco.peer.message.join import JoinHandler, CheckJoinHandler, NewMemberHandler
from LibreCisco.peer.message.msg import MessageHandler

from LibreCisco.utils import printText
from LibreCisco.utils.command import Command
from LibreCisco.utils.message import Message

class Peer(threading.Thread, Command):

    def __init__(self, host, name, role, cert, loopDelay=1, output_field=None):
        super(Peer, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay
        self.output_field = output_field

        self.cert = cert
        self.setServer(host, cert)
        self.connectlist = []
        self.connectnum = 0
        self.lock = threading.Lock()
        self.name = name
        self.role = role

        self.handler = {
            'join': JoinHandler(self),
            'checkjoin': CheckJoinHandler(self),
            'newmember': NewMemberHandler(self),
            'message': MessageHandler(self)
        }
        self.last_output = ''
        self.commands = {
            'send': SendCmd(self),
            'list': ListCmd(self)
        }

    def onProcess(self, msg_arr, **kwargs):
        msg_key = msg_arr[0]
        msg_arr = msg_arr[1:]
        if msg_key in self.commands:
            return self.commands[msg_key].onProcess(msg_arr)
        return ''

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            (conn,addr) = self.server.accept()
            
            accepthandle = threading.Thread(target=self.acceptHandle,args=(conn,addr))
            accepthandle.start()   

    def stop(self):
        self.stopped.set()
        self.sendMessage(('127.0.0.1',self.listenPort),'message', **{'msg': 'disconnect successful.'})
        self.server.close()

    #accept
    def setServer(self, host, cert):
        unwrap_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        unwrap_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        unwrap_socket.bind((host[0] , int(host[1])))
        unwrap_socket.listen(5)
        self.server = ssl.wrap_socket(unwrap_socket, certfile=cert[0], keyfile=cert[1], server_side=True)
        self.listenPort = host[1]
        printText('Peer prepared')
        printText('This peer is running with certificate at path {}'.format(cert[0]))
        printText('Please make sure other peers have same certicate to connect to this peer.')

    def acceptHandle(self,conn, addr):
        data = Message.recv(conn.recv(1024))
        if data._type in self.handler:
            self.handler[data._type].onRecv(addr, data._data)

    #send
    def sendMessage(self, host, sendType, **kwargs):
        if sendType in self.handler:
            messages = self.handler[sendType].onSend(target=host, **kwargs)
            for each in messages:
                sender = PeerConnection(message=each, cert_pem=self.cert[0], output_field=self.output_field)
                sender.start()
        else:
            printText('No such type.')

    #list
    def addConnectlist(self, peer_info):
        if not peer_info in self.connectlist:
            self.connectlist.append(peer_info)
            self.connectnum += 1
            
    def removeConnectlist(self):
        pass

