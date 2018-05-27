import threading
import time
import socket
import pickle
from Client import Client

class Peer(threading.Thread):
    def __init__(self, ListenIP='0.0.0.0', ListenPORT=8000):
        threading.Thread.__init__(self)  
        self.SetServer(ListenIP, ListenPORT)
        self.connectlist=[]
    def run(self):
        self.ServerAccept()

    #server
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
     
        if dataT=='newlist':
            Data = conn.recv(1024)
            datalist = pickle.loads(Data)
            for data in datalist:
                jmp=False
                for mydata in self.connectlist:
                    if mydata==data:
                        jmp=True
                        break
                if jmp==True:
                    continue
                self.connectlist.insert(0,data)
            print("server get:", self.connectlist)    
        else:
            Data = conn.recv(1024)
            data = Data.decode('ascii')
            conn.send(b"the server say: server received you message.")
            print ("server get:", data)
            if dataT=='join':
                self.connectlist.insert( 0, (data,addr[0],8000) )
                self.UploadNewList()
                print("server say:",'a peer join')


    #client sendtype
    def command(self,ip, pt, cmd):
        Sendcmd = Client(ip, pt, 'command', cmd.encode('ascii'))
        Sendcmd.start()

    def JoinNetWork(self,linkip,linkport,name):
        if name==None:
            name = 'no name'
        Sendcmd = Client(linkip, linkport, 'join',name.encode('ascii'))
        Sendcmd.start()
    
    def UploadNewList(self):
        data = pickle.dumps(self.connectlist)
        for i in range( len(self.connectlist)):
            Sendcmd = Client(self.connectlist[i][1],self.connectlist[i][2],'newlist',data)
            Sendcmd.start()

    def Exit(self):
        data = b'I leave'
        for i in self.connectlist:
            Sendcmd = Client(self.connectlist[i][1],self.connectlist[i][2], 'message', data)
            Sendcmd.start()