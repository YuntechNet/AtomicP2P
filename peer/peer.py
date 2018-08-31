import threading
import time
import socket
import pickle
import sys
from peer.connection import PeerConnection

class Peer(threading.Thread):
    def __init__(self, ip='0.0.0.0', port=8000, name='none'):
        threading.Thread.__init__(self)  
        self.setServer(ip, port)
        self.connectlist=[]
        self.connectnum=0
        self.lock = threading.Lock()
        self.name = name

    def run(self):
        while True:
            (conn,addr) = self.server.accept()           
            accepthandle = threading.Thread(target=self.acceptHandle,args=(conn,addr))
            accepthandle.start()   

    #accept
    def setServer(self,listenIp,listenPort):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(( listenIp , int(listenPort) ))
        self.server.listen(5)
        self.listenPort = listenPort
        print("server has prepared~")

    def acceptHandle(self,conn, addr):
        print('get link from',addr,'.')
        data = (pickle.loads(conn.recv(1024)))
        print ("server get:", data)
        conn.send(b'get message.')
    
        #join event
        if data[0] == 'join':
            for member in self.connectlist:
                self.sendMessage(member[2],member[1],'joindata',[data[1], addr[0]])
            self.addConnectlist(data[1],addr[0])
            self.sendMessage(addr[0],data[1][1],'checkjoin',[self.name, self.listenPort])
        elif data[0] == 'joindata':
            self.addConnectlist(data[1][0],data[1][1])
            self.sendMessage(data[1][1],data[1][0][1],'checkjoin',[self.name, self.listenPort])
        elif data[0] == 'checkjoin':
            self.addConnectlist(data[1],addr[0])
    
    #send
    def sendMessage(self, ip, port, sendType, message):
        sender = PeerConnection( ip, port, sendType, message)
        sender.start()

    #list
    def addConnectlist(self, member, ip):
        check=True
        for listmember in self.connectlist:
            if self.connectlist != []:
                if member[1] == listmember[1]:
                    check = False
                    break
        if member[1]==self.listenPort:
            check = False  
        if check == True:
            member.append(ip)
            self.connectlist.append(member)
            self.connectnum += 1
            
    def removeConnectlist(self):
        pass
