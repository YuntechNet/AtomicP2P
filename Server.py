from Config import Config
import sys, socket


class LibServer:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created on host: %s' % HOST)

        try:
            self.sock.bind((self.host, self.port))
        except socket.error as err:
            print('Bind failed. Error Code : ' .format(err))

        self.sock.listen(10)
        print("Socket Listening on port %d" % self.port)

        self.stopSig = False

    def loop(self):
        try:
            conn, addr = self.sock.accept()
            conn.send(bytes("Message"+"\r\n",'UTF-8'))
            print("Message sent")
            data = conn.recv(1024)
            print(data.decode(encoding='UTF-8'))
        except socket.error as e:
            self.sock.close()
            print(e)
        return self.loop() if self.stopSig == False else None

    def start(self):
        self.loop()

    def stop(self):
        self.stopSig = True

HOST = Config.SERVER_HOST
PORT = Config.SERVER_PORT

for each in sys.argv:
    if '--HOST=' in each:
        HOST = str(each[7:])
    elif '--PORT=' in each:
        PORT = int(each[7:])

libServer = LibServer(HOST, PORT)
libServer.loop()
