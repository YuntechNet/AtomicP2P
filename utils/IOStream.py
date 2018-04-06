import os, time, logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from Config import Config
from network.Command import Command, Commander
from utils.logging import LibCiscoLogger
from utils.Manager import ThreadManager
from utils.Enums import CommandType

class OutputStream(ThreadManager):

    def __init__(self, inputStream, outputQueue, argv=[], config=Config):
        ThreadManager.__init__(self, 'OutputStream', outputQueue)

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return
        self.loadArgv(argv)
        self.initLogging()
        self.inputStream = inputStream
        self.print('Inited.', logging.INFO)

    def run(self):
        while not self.stopped.wait(0.01) or not self.outputQueue.empty():
            if not self.outputQueue.empty():
                msg = self.outputQueue.get()
                (time, level, process, msg) = (datetime.fromtimestamp(msg[0]).strftime('%Y-%m-%d %H:%M:%S.%f'), msg[1], msg[2], msg[3])
                self.logger.log(level, msg, extra={'execute_time': time, 'process_name': process})
            elif self.inputStream.isExit():
                self.exit()
        os.system('kill %d' % os.getpid())

    def loadConfig(self, config=Config):
        self.print('Loading config', logging.DEBUG)
        if hasattr(config, 'OUTPUT'):
            self.config = config.OUTPUT
            self.logConfig = self.config['LOG']
            self.logLevel = self.logConfig['LEVEL']
            self.logFolder = self.logConfig['FOLDER']
            self.logSize = self.logConfig['SIZE_PER_FILE']
            self.logCount = self.logConfig['MAX_BACKUP_COUNT']
            self.print('Config loaded.', logging.DEBUG)
            return True
        else:
            self.print('Config must contain OUTPUT attribute.', logging.ERROR)
            return False

    def loadArgv(self, argv):
        self.print('Loading argv', logging.DEBUG)
        for each in argv:
            if '--log-level=' in each:
                self.logLevel = each[12:]
            elif '--log-folder=' in each:
                self.logFolder = each[13:]
            elif '--log-size=' in each:
                self.logSize = each[11:]
            elif '--log-count=' in each:
                self.logCount = each[12:]
        self.print('Argv loaded.', logging.DEBUG)
        
    def initLogging(self):
        self.print('Initing Logger.', logging.DEBUG)
        logFormat = logging.Formatter('[%(execute_time)s |%(levelname)8s | %(process_name)s] %(message)s')
        fileHwnd = RotatingFileHandler(self.logFolder, mode='a', maxBytes=self.logSize, backupCount=self.logCount)
        fileHwnd.setFormatter(logFormat)
        fileHwnd.setLevel(getattr(logging, self.logLevel))
        
        consoleHwnd = logging.StreamHandler()
        consoleHwnd.setFormatter(logFormat)
        consoleHwnd.setLevel(getattr(logging, self.logLevel))

        logging.setLoggerClass(LibCiscoLogger)
        appLog = logging.getLogger('LibCisco')
        appLog.setLevel(getattr(logging, self.logLevel))
        appLog.addHandler(fileHwnd)
        appLog.addHandler(consoleHwnd)
        self.logger = appLog
        self.print('Logger inited', logging.DEBUG)

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
            Commander.processReq(self.redis, 'LibCisco-Redis', choice, None)
        elif '--switch' in choice:
            Commander.processReq(self.redis, 'SwitchManager-Redis', choice, None)
        elif '--schedule' in choice:
            Commander.processReq(self.redis, 'ScheduleManager-Redis', choice, None)
        elif '--libserver' in choice:
            Commander.processReq(self.redis, 'LibServer-Redis', choice, None)
        elif '--broadcast' in choice:
            Commander.processReq(self.redis, ['LibCisco-Redis', 'SwitchManager-Redis', 'ScheduleManager-Redis', 'LibServer-Redis'], choice, None)
        else:
            Commander.processReq(self.redis, None, choice, None)

