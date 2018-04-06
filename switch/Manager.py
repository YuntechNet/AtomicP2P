import logging

from Config import Config
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

    def __init__(self, outputQueue, argv=[], sleep=1, config=Config):
        ProcessManager.__init__(self, 'SwitchManager', outputQueue)
        self.sleep = sleep

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return
        self.print('Inited.', logging.INFO)

    def start(self, instance):
        self.instance = instance
        self.databaseManager.start()
        super(SwitchManager, self).start()

    def loadConfig(self, config=Config):
        self.print('Loading config', logging.DEBUG)
        if hasattr(config, 'SWITCH_MANAGER'):
            self.devices = {}
            self.config = config.SWITCH_MANAGER
            self.databaseManager = SwitchDatabaseManager(self.outputQueue, self.config)
            if 'STATIC' in self.config:
                for each in self.config['STATIC']:
                    sw = Switch(each)
                    self.devices[sw.host] = sw
                self.print('STATIC devices loaded.', logging.DEBUG)
            self.print('Config loaded.', logging.DEBUG)
            return True
        else:
            self.print('Config must contain SWITCH_MANAGER attribute.', logging.ERROR)
            return False


    def getDeviceByHost(self, host):
        if host == 'ALL':
            return [ value for (key, value) in self.devices.items() ]
        else:
            for (key, value) in self.devices.items():
                if value.host == host:
                    return [ value ]
        return None

    def run(self):
        while not self.stopped.wait(self.sleep):
            self.toSystem()

    def toSystem(self):
        self.devices = {}
        if self.databaseManager.remoteDB.type == 'mongodb':
            from bson.json_util import loads as bsonLoads
            result = self.databaseManager.temporDB.execute('SELECT * FROM `Switch`').fetchall()
            for (host, jsonContent) in result:
                bsonContent = bsonLoads(jsonContent)
                bsonContent['host'] = host
                self.devices[host] = Switch(bsonContent)
        elif self.databaseManager.remoteDB.type == 'mysql':
            pass
        else:
            pass

    def exit(self):
        self.databaseManager.exit()
        super(SwitchManager, self).exit()

