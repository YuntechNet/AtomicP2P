import sys, time
from queue import Queue
from Config import Config
from switch.Manager import SwitchManager
from server.Server import LibServer

if __name__ == '__main__':

    LIB_HOST = Config.LIB_SERVER['HOST']
    LIB_PORT = Config.LIB_SERVER['PORT']

    msgQueue = Queue()

    switchManager = SwitchManager(msgQueue)
    switchManager.start()

    for each in sys.argv:
        if '--LIB_HOST=' in each:
            LIB_HOST = str(each[7:])
        elif '--LIB_PORT=' in each:
            LIB_PORT = int(each[7:])
    
    libServer = LibServer(msgQueue, LIB_HOST, LIB_PORT)
    libServer.start()

    while(True):
        if not msgQueue.empty():
            (msg, timestamp) = msgQueue.get()
            print('[%s] %s' % (timestamp, msg))
        time.sleep(1)
