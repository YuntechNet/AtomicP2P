import sys
from Config import Config
from server.Server import LibServer

if __name__ == '__main__':

    HOST = Config.LIBSERVER_HOST
    PORT = Config.LIBSERVER_PORT
    
    for each in sys.argv:
        if '--HOST=' in each:
            HOST = str(each[7:])
        elif '--PORT=' in each:
            PORT = int(each[7:])
    
    libServer = LibServer(HOST, PORT)
    libServer.start()
