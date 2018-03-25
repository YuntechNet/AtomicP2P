import sys, traceback

from queue import Queue
from core.LibCisco import LibCisco
from switch.Manager import SwitchManager
from server.Server import LibServer
from schedule.Manager import ScheduleManager
from communicate.Manager import RedisManager
from communicate.Command import Command
from utils.IOStream import InputStream, OutputStream

if __name__ == '__main__':

    try:
        instance = {}
        outputQueue = Queue()

        inputStream = InputStream(outputQueue)
        outputStream = OutputStream(inputStream, outputQueue)

        for each in sys.argv:
            if '--Core' in each:
                libCisco = LibCisco(outputQueue, argv=sys.argv, callback=inputStream.mainProcessCallback)
                libCisco.start()
                instance['libCisco'] = libCisco
                inputStream.redis = libCisco.redis
            elif '--SwitchManager' in each:
                switchManager = SwitchManager(outputQueue, argv=sys.argv, callback=inputStream.mainProcessCallback)
                switchManager.start()
                instance['switchManager'] = switchManager
                inputStream.redis = switchManager.redis
            elif '--ScheduleManager' in each:
                scheduleManager = ScheduleManager(outputQueue, argv=sys.argv, callback=inputStream.mainProcessCallback)
                scheduleManager.start()
                instance['scheduleManager'] = scheduleManager
                inputStream.redis = scheduleManager.redis
            elif '--LibServer' in each:
                libServer = LibServer(outputQueue, argv=sys.argv, callback=inputStream.mainProcessCallback)
                libServer.start()
                instance['libServer'] = libServer
                inputStream.redis = libServer.redis

        if instance == {}:
            libCisco = LibCisco(outputQueue, argv=sys.argv, callback=inputStream.mainProcessCallback)
            switchManager = SwitchManager(outputQueue, argv=sys.argv, callback=inputStream.mainProcessCallback)
            scheduleManager = ScheduleManager(outputQueue, argv=sys.argv, callback=inputStream.mainProcessCallback)
            libServer = LibServer(outputQueue, argv=sys.argv, callback=inputStream.mainProcessCallback)
            inputStream.redis = libCisco.redis
            instance = {
                'libCisco': libCisco,
                'switchManager': switchManager,
                'scheduleManager': scheduleManager,
                'libServer': libServer
            }
            [ value.start() for (key, value) in instance.items() ]

        instance['inputStream'] = inputStream
        inputStream.instance = instance
        inputStream.start()

        outputStream.start()

        #inputStream.redis.pubAll(inputStream.redis.name, 'online-signal')
        outputStream.join()
    except:
        traceback.print_exc()
    
