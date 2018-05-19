import threading
import time
import socket

class SCjudge:
    #link_D = {'myself':'192.168.0.0'}
    def __init__(self, IP_D):
        self.first=0
        self.link_D = {'myself':'0.0.0.0'}
        
        if IP_D.keys == None:
            print("I don't have. I am lonely~")
            self.first=1
        
        else:
            print("I have " , IP_D)
            for k in IP_D.keys():
                print(k)
                self.link_D[k]=IP_D[k]        
        
        print (self.link_D)

    def check(slef, key): 
        print('hey')
'''
    #server and client

    def server(self, HOST, PORT):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        print("wait for connect~")
        while True:
            (conn,addr) = s.accept()
            print('hey ',addr)
            while True:
                data = conn.recv(1024)
                check=1
                print (data.decode('ascii'))
                conn.send(b"server received you message.")

    def client(self, HOST,PORT):
        h = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        h.connect((HOST, PORT))

        while True:
            cmd = input("Please input msg:")
            h.send(cmd.encode('ascii'))
            data = h.recv(1024)
            print (data.decode('ascii'))
            if data.decode('ascii')=="server received you message.":
                break
        return
'''
class client(threading.Thread):
    def __init__(self, HOST,PORT):
        threading.Thread.__init__(self)
        self.h = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.h.connect((HOST, PORT))
        self.finish=False

    def create_c(self):
        while True:
            cmd = '7000'#input("Please input msg:")
            self.h.send(cmd.encode('ascii'))
            data = self.h.recv(1024)
            print (data.decode('ascii'))
            if data.decode('ascii')=="server received you message.":
                self.finish=True
                break
        return

class Command(client):
    def __init__(self):
        threading.Thread.__init__(self)    

    def command(self):
        cmd = input('imput what do you want to do:')
        if cmd=='help':
            print('S: send your message to aim.')
        elif cmd == 'S':
            ip = str(input ('what the host do you want to send:'))
            pt = int(input ('what the port do you use:'))
            print(ip," ",pt)
            t_s = threading.Thread(target = client(ip,pt))
            t_s.start()

if __name__ == '__main__' :
    IP_dictionary = {'switch maneger':'192.168.43.53'}
    test = SCjudge(IP_dictionary)
    '''
    print(test.link_D['myself'])
    
    test.server(test.link_D['myself'],7000)
    '''
    t2 = client("192.168.43.53",8000)
    t2.start()
    t2.create_c()
    t2._stop()
    #tc = Command()
    #tc.start()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((test.link_D['myself'], 7000))
    s.listen(1)
    print("wait for connect~")
    while True:
        (conn,addr) = s.accept()
        #tc.command()
        print('hey ',addr)
        #while True:
        data = conn.recv(1024)
        print (data.decode('ascii'))
        conn.send(b"server received you message.")
        t1 = client(addr[0],8000)
        t1.start()
        t1.create_c()
        t1._stop()