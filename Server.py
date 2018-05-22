import threading
import time
import socket
from Client import Client 


class Server(threading.Thread):
    def __init__(self, MyIP, Myhost):
        threading.Thread.__init__(self)  
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((MyIP, Myhost))
        self.server.listen(1)
        print(MyIP,Myhost,"server has prepared~")

    def run(self):
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
        data = self.Conn.recv(1024)
        print (data.decode('ascii'))
        self.Conn.send(b"server received you message.")
