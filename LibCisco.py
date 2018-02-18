import sys
from Config import Config
from Server import LibServer

if __name__ == '__main__':

    HOST = Config.SERVER_HOST
    PORT = Config.SERVER_PORT
    
    for each in sys.argv:
        if '--HOST=' in each:
            HOST = str(each[7:])
        elif '--PORT=' in each:
            PORT = int(each[7:])
    
    libServer = LibServer(HOST, PORT)
    libServer.start()
    libServer.stop()
