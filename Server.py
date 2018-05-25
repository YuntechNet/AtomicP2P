import threading
import time
import socket
from Client import Client 


class Server(threading.Thread):
    def __init__(self, MyIP, MyPORT, IP, PORT):
        threading.Thread.__init__(self)  
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', int(MyPORT) ))
        self.server.listen(5)
        
        self.ip = IP
        self.port = PORT
        self.IPlist = [(MyIP, MyPORT)]
        print("server has prepared~")

    def run(self):
        if( self.ip!="" and self.port!=""):
            print('handshake to ', self.ip, self.port)
            sendmyip = self.IPlist[0][0] + ' ' + self.IPlist[0][1]
            Handshake = Client(self.ip, int(self.port), 'handshake', sendmyip)
            Handshake.start()
        while True:
            (conn,addr) = self.server.accept()           
            Accepthandle = AcceptHandle(conn,addr)
            Accepthandle.start()

class AcceptHandle(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.Conn = conn
        self.Addr = addr

    def run(self):
        print('get link from',self.Addr,'.')
        DataT = self.Conn.recv(1024)
        dataT = DataT.decode('ascii')
        self.Conn.send(b"server know what's type you may send.")
        print (dataT)
        
        Data = self.Conn.recv(1024)
        data = Data.decode('ascii')
        self.Conn.send(b"server received you message.")
        print (data)
        