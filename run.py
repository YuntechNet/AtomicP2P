import sys, traceback

from queue import Queue
from LibCisco import LibCisco
from switch.Manager import SwitchManager
from server.Server import LibServer
from schedule.Manager import ScheduleManager
from database.Manager import RedisManager
from utils.Task import Task
from utils.IOStream import InputStream, OutputStream

if __name__ == '__main__':

    try:
        instance = {}
        outputQueue = Queue()

        for each in sys.argv:
            if '--Core' in each:
                libCisco = LibCisco(outputQueue, sys.argv)
                libCisco.start()
                instance['libCisco'] = libCisco
                redisManager = libCisco.redisManager
            elif '--SwitchManager' in each:
                switchManager = SwitchManager(outputQueue, sys.argv)
                switchManager.start()
                instance['switchManager'] = switchManager
                redisManager = switchManager.redisManager
            elif '--ScheduleManager' in each:
                scheduleManager = ScheduleManager(outputQueue, sys.argv)
                scheduleManager.start()
                instance['scheduleManager'] = scheduleManager
                redisManager = scheduleManager.redisManager
            elif '--LibServer' in each:
                libServer = LibServer(outputQueue, sys.argv)
                libServer.start()
                instance['libServer'] = libServer
                redisManager = libServer.redisManager

        if instance == {}:
            libCisco = LibCisco(outputQueue, sys.argv)
            switchManager = SwitchManager(outputQueue, sys.argv)
            scheduleManager = ScheduleManager(outputQueue, sys.argv)
            libServer = LibServer(outputQueue, sys.argv)
            redisManager = libCisco.redisManager
            instance = {
                'libCisco': libCisco,
                'switchManager': switchManager,
                'scheduleManager': scheduleManager,
                'libServer': libServer
            }
            [ value.start() for (key, value) in instance.items() ]

        inputStream = InputStream(redisManager, instance, outputQueue)
        inputStream.start()
        instance['inputStream'] = inputStream

        outputStream = OutputStream(inputStream, outputQueue)
        outputStream.start()
        outputStream.join()
    except:
        traceback.print_exc()
    
