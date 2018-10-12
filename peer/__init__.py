import threading
import time
import socket
import pickle
import sys

from threading import Event

from peer.peer_info import PeerInfo
from peer.connection import PeerConnection
from peer.message import Message
from peer.message.join import JoinHandler, CheckJoinHandler, NewMemberHandler
from peer.message.msg import MessageHandler, BroadcastHandler

class Peer(threading.Thread):
    def __init__(self, ip='0.0.0.0', port=8000, name='none', role='core', loopDelay=1):
        super(Peer, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay

        self.setServer(ip, port)
        self.connectlist = []
        self.connectnum = 0
        self.lock = threading.Lock()
        self.name = name
        self.role = role

        self.handler = {
            'join': JoinHandler(self),
            'checkjoin': CheckJoinHandler(self),
            'newmember': NewMemberHandler(self),
            'message': MessageHandler(self),
            'broadcast': BroadcastHandler(self)
        }
        self.last_output = ''

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
    def setServer(self,listenIp,listenPort):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((listenIp , int(listenPort)))
        self.server.listen(5)
        self.listenPort = listenPort
        print("server prepared")

    def acceptHandle(self,conn, addr):
        data = Message.recv(conn.recv(1024))
        if data._type in self.handler:
            self.handler[data._type].onRecv(addr, data._data)
            conn.send(b'')

    #send
    def sendMessage(self, host, sendType, **kwargs):
        if sendType in self.handler:
            message = self.handler[sendType].onSend(target=host, **kwargs)
            sender = PeerConnection(message)
            sender.start()
        else:
            print('No such type.')

    #list
    def addConnectlist(self, peer_info):
        if not peer_info in self.connectlist:
            self.connectlist.append(peer_info)
            self.connectnum += 1
            
    def removeConnectlist(self):
        pass

