import threading
import socket

from threading import Event

from peer.peer_info import PeerInfo
from peer.connection import PeerConnection
from peer.command import SendCmd, ListCmd
from peer.message.join import JoinHandler, CheckJoinHandler, NewMemberHandler
from peer.message.msg import MessageHandler

from utils import printText
from utils.command import Command
from utils.message import Message

class Peer(threading.Thread, Command):

    def __init__(self, host, name, role, loopDelay=1, output_field=None):
        super(Peer, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay
        self.output_field = output_field

        self.setServer(host)
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
    def setServer(self, host):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host[0] , int(host[1])))
        self.server.listen(5)
        self.listenPort = host[1]
        printText("server prepared")

    def acceptHandle(self,conn, addr):
        data = Message.recv(conn.recv(1024))
        if data._type in self.handler:
            self.handler[data._type].onRecv(addr, data._data)
            conn.send(b'')

    #send
    def sendMessage(self, host, sendType, **kwargs):
        if sendType in self.handler:
            messages = self.handler[sendType].onSend(target=host, **kwargs)
            for each in messages:
                sender = PeerConnection(message=each, output_field=self.output_field)
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

