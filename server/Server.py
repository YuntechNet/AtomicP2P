import socket

from Config import Config
from utils.Enums import LogLevel
from utils.Manager import ProcessManager
from database.Manager import RedisManager

class LibServer(ProcessManager):

    def __init__(self, outputQueue, argv=None, sleep=0.5):
        ProcessManager.__init__(self, 'LibServer', outputQueue)
        self.sleep = sleep
        self.loadArgv(argv)

        self.redisManager = RedisManager('LibServer', ['LibServer'], outputQueue, self.command)
        self.redisManager.start()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.print('Socket created on host: %s' % self.host)

        try:
            self.sock.bind((self.host, self.port))
        except socket.error as err:
            self.print('Bind failed. Error Code : ' .format(err))

        self.sock.listen(10)
        self.print("Socket Listening on port %d" % self.port)

    def loadArgv(self, argv):
        self.host = Config.LIB_SERVER['HOST']
        self.port = Config.LIB_SERVER['PORT']
        if not argv is None:
            for each in argv:
                if '--LIB_HOST' in each:
                    self.host = str(each[7:])
                elif '--LIB_PORT' in each:
                    self.port = str(each[7:])

    def run(self): # Override
        while not self.stopped.wait(self.sleep):
            conn, addr = self.sock.accept()
            try:
                conn.send(bytes("Message"+"\r\n",'UTF-8'))
                self.print("Message sent")
                data = conn.recv(1024)
                self.print(data.decode(encoding='UTF-8'))
            except socket.error as e:
                self.print(e)
            self.sock.close()

    def command(self, command):
        if 'heart-beat' in command:
            self.print('Heart Beat: %s' % command)

    # The best way to stop a block-socket server is connect to itself and close
    # connection to let code keep running to next loop to detect stop signal.
    def exit(self):
        self.redisManager.exit()
        super(LibServer, self).exit()
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
        self.sock.close()

