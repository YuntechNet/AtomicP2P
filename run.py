import sys, traceback

from queue import Queue
from core.LibCisco import LibCisco
from switch.Manager import SwitchManager
from server.Server import LibServer
from schedule.Manager import ScheduleManager
from status.Manager import StatusManager
from network.Manager import RedisManager
from network.Command import Command
from utils.IOStream import InputStream, OutputStream

def main(argv, debug=False):
    try:
        instance = {}
        outputQueue = Queue()

        if '--LibCisco' in argv:
            redis = RedisManager('LibCisco-Redis', ['Status', 'LibCisco-Redis', 'SwitchManager-Redis', 'ScheduleManager-Redis', 'LibServer-Redis'], outputQueue)
            instance['redisManager'] = redis
            status = StatusManager(outputQueue, argv=argv)
            instance['statusManager'] = status
            libCisco = LibCisco(outputQueue, argv=argv)
            instance['libCisco'] = libCisco
        elif '--SwitchManager' in argv:
            redis = RedisManager('SwitchManager-Redis', ['Status', 'SwitchManager-Redis'], outputQueue)
            instance['redisManager'] = redis
            status = StatusManager(outputQueue, argv=argv)
            instance['statusManager'] = status
            switchManager = SwitchManager(outputQueue, argv=argv)
            instance['switchManager'] = switchManager
        elif '--ScheduleManager' in argv:
            redis = RedisManager('ScheduleManager-Redis', ['Status', 'ScheduleManager-Redis'], outputQueue)
            instance['redisManager'] = redis
            status = StatusManager(outputQueue, argv=argv)
            instance['statusManager'] = status
            scheduleManager = ScheduleManager(outputQueue, argv=argv)
            instance['scheduleManager'] = scheduleManager
        elif '--LibServer' in argv:
            redis = RedisManager('LibServer-Redis', ['Status', 'LibServer-Redis'], outputQueue)
            instance['redisManager'] = redis
            status = StatusManager(outputQueue, argv=argv)
            instance['statusManager'] = status
            libServer = LibServer(outputQueue, argv=argv)
            instance['libServer'] = libServer
        else: #if instance == {}:
            redis = RedisManager('LibCisco-Redis', ['Status', 'LibCisco-Redis', 'SwitchManager-Redis', 'ScheduleManager-Redis', 'LibServer-Redis'], outputQueue)
            instance['redisManager'] = redis
            status = StatusManager(outputQueue, argv=argv)
            instance['statusManager'] = status
            libCisco = LibCisco(outputQueue, argv=argv)
            instance['libCisco'] = libCisco
            switchManager = SwitchManager(outputQueue, argv=argv)
            instance['switchManager'] = switchManager
            scheduleManager = ScheduleManager(outputQueue, argv=argv)
            instance['scheduleManager'] = scheduleManager
            libServer = LibServer(outputQueue, argv=argv)
            instance['libServer'] = libServer
        if not debug:
            [ value.start(instance) for (key, value) in instance.items() ]

        inputStream = InputStream(outputQueue, redis)
        instance['inputStream'] = inputStream
        inputStream.instance = instance

        outputStream = OutputStream(inputStream, outputQueue, argv)

        if not debug:
            inputStream.start()
            outputStream.start()

        return (instance, inputStream, outputStream)
    except:
        traceback.print_exc()
    
if __name__ == '__main__':
    instance, inputStream, outputStream = main(sys.argv)
    outputStream.join()
