import queue, redis

from Config import Config
from utils.Enums import LogLevel
from utils.Manager import ProcessManager
from switch.Switch import Switch
from switch.Command import SwitchCommand
from database.Manager import DatabaseManager
from network.Manager import RedisManager

class SwitchDatabaseManager(DatabaseManager):

    def __init__(self, outputQueue, config, sleep=300):
        DatabaseManager.__init__(self, outputQueue, config, sleep)

    # Override
    def sync(self):
        if self.remoteDB.type == 'mongodb':
            from bson.json_util import dumps as bsonDumps
            every = self.remoteDB.switchCol.find({})
            for doc in every:
                ip = self.remoteDB.ipCol.find_one({ '_id': doc['ipID'] })
                cmd = 'REPLACE INTO Switch(IPv4, content) VALUES (\'%s\', \'%s\');' % (ip['ipv4'], bsonDumps(doc))
                self.temporDB.execute(cmd)
        elif self.remoteDB.type == 'mysql':
            pass
        else:
            pass        

# SwitchManager
#   A process responsible for arrane switch heart-beat & execute command.
#
class SwitchManager(ProcessManager):

    def __init__(self, outputQueue, argv=None, sleep=1, callback=None, config=Config):
        ProcessManager.__init__(self, 'SwitchManager', outputQueue, callback)
        self.sleep = sleep

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return
        self.print('Config loaded.')
        self.commander = SwitchCommand(self)
        self.redis = RedisManager('SwitchManager-Redis', ['SwitchManager-Redis'], outputQueue, self.commander.process)
        self.print('Inited.', LogLevel.SUCCESS)

    def start(self):
        self.redis.start()
        self.databaseManager.start()
        super(SwitchManager, self).start()

    def loadConfig(self, config):
        self.print('Loading config')
        if hasattr(config, 'SWITCH_MANAGER'):
            self.device = []
            self.config = config.SWITCH_MANAGER
            self.databaseManager = SwitchDatabaseManager(self.outputQueue, self.config)
            if 'STATIC' in self.config:
                for each in self.config['STATIC']:
                    self.device.append(Switch(each))
                self.print('STATIC devices loaded.')
            return True
        else:
            self.print('Config must contain SWITCH_MANAGER attribute.', LogLevel.ERROR)
            return False


    def getDeviceByHost(self, host):
        for each in self.device:
            if each.config.host == host:
                return each
        return None

    def run(self):
        while not self.stopped.wait(self.sleep):
            self.toSystem()

    def toSystem(self):
        self.devices = []
        if self.databaseManager.remoteDB.type == 'mongodb':
            from bson.json_util import loads as bsonLoads
            result = self.databaseManager.temporDB.execute('SELECT * FROM `Switch`').fetchall()
            for (host, jsonContent) in result:
                config = bsonLoads(jsonContent)
                config['host'] = host
                self.devices.append(Switch(config))
        elif self.databaseManager.remoteDB.type == 'mysql':
            pass
        else:
            pass

    def exit(self):
        self.databaseManager.exit()
        self.redis.exit()
        super(SwitchManager, self).exit()

