import sys, traceback

from queue import Queue
from core.LibCisco import LibCisco
from switch.Manager import SwitchManager
from server.Server import LibServer
from schedule.Manager import ScheduleManager
from network.Manager import RedisManager
from network.Command import Command
from utils.IOStream import InputStream, OutputStream

def main(argv, debug=False):
    try:
        instance = {}
        outputQueue = Queue()

        inputStream = InputStream(outputQueue)
        outputStream = OutputStream(inputStream, outputQueue)

        for each in argv:
            if '--LibCisco' in each:
                libCisco = LibCisco(outputQueue, argv=argv, callback=inputStream.mainProcessCallback)
                instance['libCisco'] = libCisco
                inputStream.redis = libCisco.redis
            elif '--SwitchManager' in each:
                switchManager = SwitchManager(outputQueue, argv=argv, callback=inputStream.mainProcessCallback)
                instance['switchManager'] = switchManager
                inputStream.redis = switchManager.redis
            elif '--ScheduleManager' in each:
                scheduleManager = ScheduleManager(outputQueue, argv=argv, callback=inputStream.mainProcessCallback)
                instance['scheduleManager'] = scheduleManager
                inputStream.redis = scheduleManager.redis
            elif '--LibServer' in each:
                libServer = LibServer(outputQueue, argv=argv, callback=inputStream.mainProcessCallback)
                instance['libServer'] = libServer
                inputStream.redis = libServer.redis

        if instance == {}:
            libCisco = LibCisco(outputQueue, argv=argv, callback=inputStream.mainProcessCallback)
            switchManager = SwitchManager(outputQueue, argv=argv, callback=inputStream.mainProcessCallback)
            scheduleManager = ScheduleManager(outputQueue, argv=argv, callback=inputStream.mainProcessCallback)
            libServer = LibServer(outputQueue, argv=argv, callback=inputStream.mainProcessCallback)
            inputStream.redis = libCisco.redis
            instance = {
                'libCisco': libCisco,
                'switchManager': switchManager,
                'scheduleManager': scheduleManager,
                'libServer': libServer
            }
        if not debug:
            [ value.start() for (key, value) in instance.items() ]

        instance['inputStream'] = inputStream
        inputStream.instance = instance

        if not debug:
            inputStream.start()
            outputStream.start()

        #inputStream.redis.pubAll(inputStream.redis.name, 'online-signal')
        return (instance, inputStream, outputStream)
    except:
        traceback.print_exc()
    
if __name__ == '__main__':
    instance, inputStream, outputStream = main(sys.argv)
    outputStream.join()
