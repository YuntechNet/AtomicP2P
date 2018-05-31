import threading
import time
import socket
import pickle
from Connect import Connect
from Handle import Handle
from Send import Send

class Peer(threading.Thread):
    def __init__(self, ListenIP='0.0.0.0', ListenPORT=8000):
        threading.Thread.__init__(self)  
        self.Listenport=ListenPORT
        self.SetServer(ListenIP, ListenPORT)
        self.connectlist=[]
        self.lock = threading.Lock()

    def run(self):
        self.ServerAccept()

    #accept
    def SetServer(self,listenIP,listenport):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', int(listenport) ))
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
        conn.send(b"the server say: server know what's type you may send.")
        print ("server get:", dataT)
        Data = conn.recv(1024)
        
        handle=Handle(self,dataT,Data,conn, addr)
        self.lock.acquire()
        handle.typechoose()
        self.lock.release()

    #send
    def Sendmessage(self, Type, Linkip='', Linkport=0, Linkdata=None):
        send = Send(Type,Linkip,Linkport,Linkdata)
        send.sendchoose()