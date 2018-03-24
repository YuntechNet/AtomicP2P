import json, os

from Config import Config
from database.Manager import DatabaseManager, RedisManager
from schedule.Schedule import Schedule
from utils.Manager import ProcessManager
from utils.User import User
from utils.Enums import UserPriority, LogLevel

class ScheduleDatabaseManager(DatabaseManager):

    def __init__(self, outputQueue, config, sleep=300):
        DatabaseManager.__init__(self, outputQueue, config, sleep)

    # Override
    def sync(self):
        pass

# ScheduleManager
#   A process responsible for arrange schedule to execute with switch.
#
class ScheduleManager(ProcessManager):

    def __init__(self, outputQueue, argv=None, sleep=60, callback=None, config=Config):
        ProcessManager.__init__(self, 'ScheduleManager', outputQueue, callback)
        self.sleep = sleep

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return
        self.print('Config loaded.')
        self.redisManager = RedisManager('ScheduleManager-Redis', ['ScheduleManager-Redis'], outputQueue, self.command)

        self.schedules = {}
        self.user = User('system.scheduler', UserPriority.SCHEDULE)
        self.toSystem()
        self.print('Inited.', LogLevel.SUCCESS)

    def start(self):
        self.redisManager.start()
        self.databaseManager.start()
        super(ScheduleManager, self).start()

    def loadConfig(self, config):
        self.print('Loading config')
        if hasattr(config, 'SCHEDULE_MANAGER'):
            self.config = config.SCHEDULE_MANAGER
            self.databaseManager = ScheduleDatabaseManager(self.outputQueue, self.config)
            return True
        else:
            self.print('Config must contain SCHEDULE_MANAGER attribute.', LogLevel.ERROR)
            return False

    def loadFolder(self, path=None, overwrite=False):
        path = path if path else './schedule/static/'
        for filename in os.listdir(path if path else './schedule/static/'):
            if os.path.isfile(path + filename):
                fileConn = open(path + filename)
                jsonContent = fileConn.read()

                if not filename in self.schedules:
                    self.schedules[filename] = Schedule(filename, self.outputQueue, json.loads(jsonContent))
                    self.temporDB.execute('INSERT INTO `Schedule`(Name, content) VALUES (\'%s\', \'%s\');' % (filename, jsonContent.replace('\'', '\'\'')))
                    self.print('%s%s New schedule loaded and inserted into database.' % (path, filename))
                elif overwrite:
                    self.schedules[filename] = Schedule(filename, self.outputQueue, json.loads(jsonContent))
                    self.temporDB.execute('UPDATE `Schedule` SET content = \'%s\' WHERE Name = \'%s\';' % (jsonContent.replace('\'', '\'\''), filename))
                    self.print('%s%s Old schedule loaded and updated into database.' % (path, filename))
                else:
                    self.print('%s%s Schedule is exists, abort. add -force to overwrite.' % (path, filename))
                fileConn.close()
            else:
                self.print('%s%s folder detected, ignore.' % (path, filename))

    def toSystem(self):
        schedulesInDB = self.databaseManager.temporDB.execute('SELECT * FROM `Schedule`').fetchall()
        for (name, jsonContent) in schedulesInDB:
            self.schedules[name] = Schedule(self, name, self.outputQueue, json.loads(jsonContent))
            self.schedules[name].start()

    def getScheduleByName(self, name):
        for (key, value) in self.schedules.items():
            if value.name == name:
                return self.schedules[key]

    def command(self, command): #Override
        if super(ScheduleManager, self).command(command) is False and self.redisManager.isMine(command):
            if 'ls' in command._content:
                [self.print('%s %s' % (key, value)) for (key, value) in self.schedules.items()]
            elif 'load-folder' in command:
                [value.exit() for (key, value) in self.schedules.items()]
                self.loadFolder(overwrite='-force' in command._content)
            elif 'start-all' in command._content:
                [value.start() for (key, value) in self.schedules.items()]
            elif 'stop-all' in command._content:
                [value.exit() for (key, value) in self.schedules.items()]
            else:
                self.redisManager.print(command.to())

    def run(self):
        while not self.stopped.wait(self.sleep):
            pass

    def exit(self):
        for (name, instance) in self.schedules.items():
            instance.exit()
        self.redisManager.exit()
        self.databaseManager.exit()
        super(ScheduleManager, self).exit()

