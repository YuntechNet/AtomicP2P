import sys
from Config import Config
from switch.Manager import SwitchManager
from server.Server import LibServer

if __name__ == '__main__':

    LIB_HOST = Config.LIB_SERVER['HOST']
    LIB_PORT = Config.LIB_SERVER['PORT']

    switchManager = SwitchManager()
    switchManager.start()

    for each in sys.argv:
        if '--LIB_HOST=' in each:
            LIB_HOST = str(each[7:])
        elif '--LIB_PORT=' in each:
            LIB_PORT = int(each[7:])
    
    libServer = LibServer(LIB_HOST, LIB_PORT)
    libServer.start()
