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
                redis = RedisManager('LibCisco-Redis', ['LibCisco-Redis', 'SwitchManager-Redis', 'ScheduleManager-Redis', 'LibServer-Redis'], outputQueue)
                instance['redisManager'] = redis
            elif '--SwitchManager' in each:
                switchManager = SwitchManager(outputQueue, argv=argv)
                instance['switchManager'] = switchManager
                redis = RedisManager('SwitchManager-Redis', ['SwitchManager-Redis'], outputQueue)
                instance['redisManager'] = redis
            elif '--ScheduleManager' in each:
                scheduleManager = ScheduleManager(outputQueue, argv=argv)
                instance['scheduleManager'] = scheduleManager
                redis = RedisManager('ScheduleManager-Redis', ['ScheduleManager-Redis'], outputQueue)
                instance['redisManager'] = redis
            elif '--LibServer' in each:
                libServer = LibServer(outputQueue, argv=argv)
                instance['libServer'] = libServer
                redis = RedisManager('LibServer-Redis', ['LibServer-Redis'], outputQueue)
                instance['redisManager'] = redis

        if instance == {}:
            libCisco = LibCisco(outputQueue, argv=argv)
            switchManager = SwitchManager(outputQueue, argv=argv)
            scheduleManager = ScheduleManager(outputQueue, argv=argv)
            libServer = LibServer(outputQueue, argv=argv)
            instance = {
                'libCisco': libCisco,
                'switchManager': switchManager,
                'scheduleManager': scheduleManager,
                'libServer': libServer
            }
            redis = RedisManager('LibCisco-Redis', ['LibCisco-Redis', 'SwitchManager-Redis', 'ScheduleManager-Redis', 'LibServer-Redis'], outputQueue)
            instance['redisManager'] = redis
        if not debug:
            #[ value.start(instance) for (key, value) in instance.copy().items() ]
            [ value.start(instance) for (key, value) in instance.items() ]

        inputStream = InputStream(outputQueue, redis)
        instance['inputStream'] = inputStream
        inputStream.instance = instance

        outputStream = OutputStream(inputStream, outputQueue)

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
