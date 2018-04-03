import os, time, logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from Config import Config
from network.Command import Command, Commander
from utils.logging import LibCiscoLogger
from utils.Manager import ThreadManager
from utils.Enums import CommandType

class OutputStream(ThreadManager):

    def __init__(self, inputStream, outputQueue, config=Config):
        ThreadManager.__init__(self, 'OutputStream', outputQueue)

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return
        self.initLogging()
        self.inputStream = inputStream
        self.print('Inited.', logging.INFO)

    def run(self):
        while not self.stopped.wait(0.1) or not self.outputQueue.empty():
            if not self.outputQueue.empty():
                #print('[%17f]%s %s\x1b[0m' % self.outputQueue.get())
                msg = self.outputQueue.get()
                (time, level, process, msg) = (datetime.fromtimestamp(msg[0]).strftime('%Y-%m-%d %H:%M:%S.%f'), msg[1], msg[2], msg[3])
                self.logger.log(level, msg, extra={'execute_time': time, 'process_name': process})
            elif self.inputStream.isExit():
                self.exit()
        os.system('kill %d' % os.getpid())

    def loadConfig(self, config=Config):
        self.print('Loading config')
        if hasattr(config, 'OUTPUT'):
            self.config = config.OUTPUT
            self.logConfig = self.config['LOG']
            self.print('Config loaded.')
            return True
        else:
            self.print('Config must contain OUTPUT attribute.', logging.ERROR)
            return False
        
    def initLogging(self):
        self.print('Initing Logger.')
        logFormat = logging.Formatter('[%(execute_time)s |%(levelname)8s | %(process_name)s]%(message)s')
        #fileHwnd = logging.FileHandler(self.logConfig['FOLDER'])
        fileHwnd = RotatingFileHandler(self.logConfig['FOLDER'], mode='a', maxBytes=self.logConfig['SIZE_PER_FILE'], backupCount=self.logConfig['MAX_BACKUP_COUNT'])
        fileHwnd.setFormatter(logFormat)
        fileHwnd.setLevel(getattr(logging, self.logConfig['LEVEL']))
        
        consoleHwnd = logging.StreamHandler()
        consoleHwnd.setFormatter(logFormat)
        consoleHwnd.setLevel(getattr(logging, self.logConfig['LEVEL']))

        logging.setLoggerClass(LibCiscoLogger)
        appLog = logging.getLogger('LibCisco')
        appLog.setLevel(getattr(logging, self.logConfig['LEVEL']))
        appLog.addHandler(fileHwnd)
        appLog.addHandler(consoleHwnd)
        self.logger = appLog
        self.print('Logger inited')

    def exit(self):
        super(OutputStream, self).exit()
        self.outputQueue.put((time.time(), logging.INFO, self.name, 'LibCisco all Process/Thread exited, bye.'))

class InputStream(ThreadManager):
    
    def __init__(self, outputQueue, redis):
        ThreadManager.__init__(self, 'InputStream', outputQueue)
        self.outputQueue = outputQueue
        self.redis = redis
        self.print('Inited.', logging.INFO)

    def run(self):
        while not self.isExit():
            if self.outputQueue.empty():
                choice = input('> ')
                self.print('operator execute command: %s' % choice)
                self.execute(choice)

    def loadConfig(self, config=Config):
        pass

    def execute(self, choice):
        if '--libcisco' in choice:
            Commander.processReq(self.redis, 'LibCisco-Redis', choice, None, Command(self.redis.name, 'LibCisco-Redis', choice))
        elif '--switch' in choice:
            Commander.processReq(self.redis, 'SwitchManager-Redis', choice, None, Command(self.redis.name, 'SwitchManager-Redis', choice))
        elif '--schedule' in choice:
            Commander.processReq(self.redis, 'ScheduleManager-Redis', choice, None, Command(self.redis.name, 'ScheduleManager-Redis', choice))
        elif '--libserver' in choice:
            Commander.processReq(self.redis, 'LibServer-Redis', choice, None, Command(self.redis.name, 'LibServer-Redis', choice))
        elif choice == 'exit':
            for (key, values) in self.instance.items():
                values.exit()

