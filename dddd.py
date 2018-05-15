import socket
from time import sleep, time
import threading

start=time()

def server(HOST, PORT):
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
    

    

def client(HOST,PORT):
    h = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    h.connect((HOST, PORT))

    while True:
        cmd = input("Please input msg:")
        h.send(cmd.encode('ascii'))
        data = h.recv(1024)
        print (data.decode('ascii'))

def modechoose(m,IP,Port):
    if (m == "s" or m == "server"):
        server(IP,Port)
    elif (m == "c" or m == "server"):
        client(IP,Port)
    else:
        print('oops')


if __name__=='__main__':
    IP = '192.168.43.53'
    Port = 8000
    mode = input("server(s) or client(c):")
    t1=threading.Thread(target=modechoose(mode,IP,Port))

    timeout=5
    while True:
        start=time()
        t1.start()             
        check=0
        while True:
            if time()-start > timeout and check==0:
                print("error")
                #conn.send(b"are you ok?")
                break
            elif time()-start > timeout and check!=0:
                print("safe")    
                break