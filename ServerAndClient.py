import threading
import time
import socket

class Client(threading.Thread):
    def __init__(self, HOST,PORT,Message):
        threading.Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.finish=False
        self.cmd = Message

    def run(self):
        while self.finish!=True:
            self.client.send(self.cmd.encode('ascii'))
            data = self.client.recv(1024)
            print (data.decode('ascii'))
            if data.decode('ascii')=="server received you message.":
                self.finish=True
        return

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
            LinkTo = Client(addr[0],7000, 'checklink')
            LinkTo.start()

if __name__ == '__main__' :
    IP_dictionary = {'MyIP':'0.0.0.0', 'switch maneger':'192.168.43.53'}
    s = Server('0.0.0.0',8000)
    s.start()

    while True:
        cmd = input('imput what do you want to do:')
        if cmd=='help':
            print('S: send your message to aim.')
        elif cmd == 'S':
            ip = str(input ('what the host do you want to send:'))
            pt = int(input ('what the port do you use:'))
            cmd = input('imput is your command:')
            print('I send to',ip,pt)
            Sendcmd = Client(ip, pt, cmd)
            Sendcmd.start()

    

