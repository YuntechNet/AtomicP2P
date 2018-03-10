from Config import Config
from threading import Event
import threading, socket, time

class LibServer(threading.Thread):

    def __init__(self, msgQueue, host, port, sleep=0.5):
        threading.Thread.__init__(self)
        self.msgQueue = msgQueue
        self.stopped = Event()
        self.sleep = sleep

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.print('Socket created on host: %s' % host)

        try:
            self.sock.bind((self.host, self.port))
        except socket.error as err:
            self.print('Bind failed. Error Code : ' .format(err))

        self.sock.listen(10)
        self.print("Socket Listening on port %d" % self.port)

    def print(self, msg):
        self.msgQueue.put(('[LibServer] %s' % msg, time.time()))

    def run(self): # Override
        while not self.stopped.wait(self.sleep):
            try:
                conn, addr = self.sock.accept()
                conn.send(bytes("Message"+"\r\n",'UTF-8'))
                self.print("Message sent")
                data = conn.recv(1024)
                self.print(data.decode(encoding='UTF-8'))
            except socket.error as e:
                self.sock.close()
                self.print(e)

    def stop(self):
        self.stopped.set()
