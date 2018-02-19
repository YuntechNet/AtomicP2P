from Config import Config
import threading, socket, time


class LibServer(threading.Thread):

    def __init__(self, host, port, sleep=0):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.sleep = sleep
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created on host: %s' % host)

        try:
            self.sock.bind((self.host, self.port))
        except socket.error as err:
            print('Bind failed. Error Code : ' .format(err))

        self.sock.listen(10)
        print("Socket Listening on port %d" % self.port)

        self.stopSig = False

    def run(self): # Override
        try:
            conn, addr = self.sock.accept()
            conn.send(bytes("Message"+"\r\n",'UTF-8'))
            print("Message sent")
            data = conn.recv(1024)
            print(data.decode(encoding='UTF-8'))
        except socket.error as e:
            self.sock.close()
            print(e)
        time.sleep(self.sleep)

