import threading
import time
import socket
from Client import Client 

class Server(threading.Thread):
    LinkRecord ={}
    def __init__(self, MyIP, Myhost):
        threading.Thread.__init__(self)  
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((MyIP, Myhost))
        self.server.listen(1)
        print(MyIP,Myhost,"server has prepared~")

    def run(self):
        while True:
            (conn,addr) = self.server.accept()
            print('get link from',addr,'.')
            data = conn.recv(1024)
            print (data.decode('ascii'))
            conn.send(b"server received you message.")
            #原本要藉由確認dictionary是否有此addr來執行 先以判斷是否收到checklink 
            if data.decode('ascii') != 'checklink':
                LinkTo = Client(addr[0],7000, 'checklink')
                LinkTo.start()

