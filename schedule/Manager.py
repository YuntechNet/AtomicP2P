import json, os

from Config import Config
from database.Manager import DatabaseManager
from network.Manager import RedisManager
from schedule.Schedule import Schedule
from schedule.Command import ScheduleCommand
from utils.Manager import ProcessManager
from utils.User import User
from utils.Enums import UserPriority, LogLevel, CommandType

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
        self.commander = ScheduleCommand(self)
        self.redis = RedisManager('ScheduleManager-Redis', ['ScheduleManager-Redis'], outputQueue, self.commander.process)

        self.schedules = {}
        self.user = User('system.scheduler', UserPriority.SCHEDULE)
        self.toSystem()
        self.print('Inited.', LogLevel.SUCCESS)

    def start(self):
        self.redis.start()
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
        for filename in os.listdir(path):
            if os.path.isfile(path + filename):
                fileConn = open(path + filename)
                jsonContent = fileConn.read()
                schedule = Schedule(self, filename, self.outputQueue, json.loads(jsonContent))

                if not filename in self.schedules and schedule:
                    self.schedules[filename] = schedule
                    self.databaseManager.temporDB.execute('INSERT INTO `Schedule`(Name, content) VALUES (\'%s\', \'%s\');' % (filename, jsonContent.replace('\'', '\'\'')))
                    self.print('%s%s New schedule loaded and inserted into database.' % (path, filename))
                elif overwrite and schedule:
                    self.schedules[filename] = schedule
                    self.temporDB.execute('UPDATE `Schedule` SET content = \'%s\' WHERE Name = \'%s\';' % (jsonContent.replace('\'', '\'\''), filename))
                    self.print('%s%s Old schedule loaded and updated into database.' % (path, filename))
                elif schedule:
                    self.print('%s%s Schedule is exists, abort. add -force to overwrite.' % (path, filename))
                fileConn.close()
            else:
                self.print('%s%s folder detected, ignore.' % (path, filename))

    def toSystem(self):
        schedulesInDB = self.databaseManager.temporDB.execute('SELECT * FROM `Schedule`').fetchall()
        for (name, jsonContent) in schedulesInDB:
            schedule = Schedule(self, name, self.outputQueue, json.loads(jsonContent))
            if not name in self.schedules and schedule:
                self.schedules[name] = schedule
                #self.schedules[name].start()

    def getScheduleByName(self, name):
        for (key, value) in self.schedules.items():
            if value.name == name:
                return self.schedules[key]

    def run(self):
        while not self.stopped.wait(self.sleep):
            pass

    def exit(self):
        for (name, instance) in self.schedules.items():
            instance.exit()
        self.redis.exit()
        self.databaseManager.exit()
        super(ScheduleManager, self).exit()

