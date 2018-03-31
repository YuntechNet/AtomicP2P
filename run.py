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

        for each in argv:
            if '--LibCisco' in each:
                libCisco = LibCisco(outputQueue, argv=argv)
                instance['libCisco'] = libCisco
                redis = RedisManager(libCisco, 'LibCisco-Redis', ['LibCisco-Redis', 'SwitchManager-Redis', 'ScheduleManager-Redis', 'LibServer-Redis'], outputQueue)
                instance['redisManager'] = redis
            elif '--SwitchManager' in each:
                switchManager = SwitchManager(outputQueue, argv=argv)
                instance['switchManager'] = switchManager
                redis = RedisManager(switchManager, 'SwitchManager-Redis', ['SwitchManager-Redis'], outputQueue)
                instance['redisManager'] = redis
            elif '--ScheduleManager' in each:
                scheduleManager = ScheduleManager(outputQueue, argv=argv)
                instance['scheduleManager'] = scheduleManager
                redis = RedisManager(scheduleManager, 'ScheduleManager-Redis', ['ScheduleManager-Redis'], outputQueue)
                instance['redisManager'] = redis
            elif '--LibServer' in each:
                libServer = LibServer(outputQueue, argv=argv)
                instance['libServer'] = libServer
                redis = RedisManager(libServer, 'LibServer-Redis', ['LibServer-Redis'], outputQueue)
                instance['redisManager'] = redis
        inputStream = InputStream(outputQueue, redis)
        outputStream = OutputStream(inputStream, outputQueue)

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
