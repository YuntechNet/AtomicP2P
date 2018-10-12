import threading
import time
import socket
import pickle
import sys

from threading import Event

from peer.peer_info import PeerInfo
from peer.connection import PeerConnection
from peer.message import Message

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

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            (conn,addr) = self.server.accept()
            
            accepthandle = threading.Thread(target=self.acceptHandle,args=(conn,addr))
            accepthandle.start()   

    def stop(self):
        self.stopped.set()
        self.sendMessage('127.0.0.1',self.listenPort,'message','disconnect successful.')
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
        #join event
        if data._type == 'join':
            _data = data._data.split(' ')
            print('new member join')
            member = _data
            ip = addr[0]
            peer_info = PeerInfo(name=member[0], role=member[2], host=(ip, member[1]))
            for member in self.connectlist:
                self.sendMessage(member.host[0], member.host[1], 'newmember', '{} {}'.format(data._data, ip))
            self.addConnectlist(peer_info)
            self.sendMessage(ip, _data[1],'checkjoin','{} {} {}'.format(self.name, self.listenPort, self.role))
            conn.send(b'join successful.')
        elif data._type == 'newmember':
            print('new member join')
            _data = data._data.split(' ')
            member = [_data[0], _data[1], _data[2]]
            ip = _data[3]
            peer_info = PeerInfo(name=member[0], role=member[2], host=(ip, member[1]))
            self.addConnectlist(peer_info)
            self.sendMessage(ip,member[1],'checkjoin', '{} {} {}'.format(self.name, self.listenPort, self.role))
            conn.send(b'')        
        elif data._type == 'checkjoin':
            _data = data._data.split(' ')
            member = _data
            ip = addr[0]
            peer_info = PeerInfo(name=member[0], role=member[2], host=(ip, member[1]))
            self.addConnectlist(peer_info)
            conn.send(b'')

        #message event
        elif data._type == 'message':
            _data = data._data.split(' ')
            member = _data
            ip = addr[0]
            print (data._type +": '"+ str(member) + "' from " + ip)
            conn.send(b'')
            
        #broadcast event
        elif data._type == 'broadcast':
            _data = data._data.split(' ')
            member = _data
            if _data[1] == self.role or _data[1] == 'all':
                print("get broadcast from '"+ _data[0] + "': " + _data[2])


    #send
    def sendMessage(self, ip, port, sendType, message):
        message = Message(_ip=(ip, int(port)), _type=sendType, _data=message)
        sender = PeerConnection('', '', '', message)
        sender.start()

    #list
    def addConnectlist(self, peer_info):
        if not peer_info in self.connectlist:
            self.connectlist.append(peer_info)
            self.connectnum += 1
            
    def removeConnectlist(self):
        pass

