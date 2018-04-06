import socket, logging

from Config import Config
from utils.Manager import ProcessManager

class LibServer(ProcessManager):

    def __init__(self, outputQueue, argv=[], sleep=0.5, config=Config):
        ProcessManager.__init__(self, 'LibServer', outputQueue)
        self.sleep = sleep

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return
        self.loadArgv(argv)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.print('Socket created on host: %s' % self.host, logging.INFO)

        try:
            self.sock.bind((self.host, self.port))
        except socket.error as err:
            self.print('Bind failed. Error Code : %s' % err, logging.ERROR)

        self.sock.listen(10)

        self.print("Socket Listening on port %d" % self.port)

    def start(self, instance):
        self.instance = instance
        super(LibServer, self).start()

    def loadConfig(self, config=Config):
        self.print('Loading config', logging.DEBUG)
        if hasattr(config, 'LIB_SERVER'):
            self.config = Config.LIB_SERVER
            self.host = self.config['HOST']
            self.port = self.config['PORT']
            self.print('Config loaded.', logging.DEBUG)
            return True
        else:
            self.print('Config must contain LIB_SERVER attribute.', logging.ERROR)
            return False

    def loadArgv(self, argv):
        self.print('Loading argv.', logging.DEBUG)
        for each in argv:
            if '--LIB_HOST=' in each:
                self.host = str(each[11:])
            elif '--LIB_PORT=' in each:
                self.port = int(each[11:])
        self.print('Argv loaded.', logging.DEBUG)

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

    # The best way to stop a block-socket server is connect to itself and close
    # connection to let code keep running to next loop to detect stop signal.
    def exit(self):
        super(LibServer, self).exit()
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
        self.sock.close()

