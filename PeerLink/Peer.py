import threading
import time
import socket
import pickle
import sys
sys.path.append("..")
from PeerLink.PeerConnection import PeerConnection
from AccepterAndSender.Accepter import Accepter
from AccepterAndSender.Sender import Sender

class Peer(threading.Thread):
    def __init__(self, listenIP='0.0.0.0', listenPORT=8000):
        threading.Thread.__init__(self)  
        self.listenport=listenPORT
        self.SetServer(listenIP, listenPORT)
        self.connectlist=[]
        self.lock = threading.Lock()

    def run(self):
        self.ServerAccept()

    #accept
    def SetServer(self,listenIP,listenPORT):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', int(listenPORT) ))
        self.server.listen(5)
        print("server has prepared~")

    def ServerAccept(self):
        while True:
            (conn,addr) = self.server.accept()           
            Accepthandle = threading.Thread(target=self.AcceptHandle,args=(conn,addr))
            Accepthandle.start()        

    def AcceptHandle(self,conn, addr):
        print("server get:",'get link from',addr,'.')
        DataT = conn.recv(1024)
        dataT = DataT.decode('ascii')
        conn.send(b"server know what's type you may send.")
        print ("server get:", dataT)
        Data = conn.recv(1024)
        
        accepter = Accepter(self,dataT,Data,conn, addr)
        accept = accepter.typechoose()
        conn.send(b"connect finish")
        if accept[0]=='new list':
            self.SaveList(accept)
        if(dataT=='join'):
            self.Sendmessage("Newlist", None, 0, self.connectlist)  
                
    
    def SaveList(self,savedata):
        self.connectlist += savedata[1:]
    
    
    #send
    def Sendmessage(self, Type, linkIP='', linkPORT=0, linkData=None):
        sender = Sender(Type,linkIP,linkPORT,linkData)
        sender.SendChoose()