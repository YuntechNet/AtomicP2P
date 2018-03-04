import threading
from threading import Event

from database.Database import RemoteDatabase

class RemoteDBManager(threading.Thread):

    def __init__(self, tempDB, config, sleep=0.5):
        threading.Thread.__init__(self)
        self.stopped = Event()
        self.sleep = sleep

        self.tempDB = tempDB
        self.remoteDB = RemoteDatabase(config)

    def print(self, msg):
        print('[RemoteDBManager] %s' % msg)

    def run(self): # Override
        while not self.stopped.wait(self.sleep):
            self.getDevices()

    def getDevices(self):
        self.print('Loading devices.')
        device = []
        if self.remoteDB.type == 'mongodb':
            every = self.remoteDB.switchCol.find({})
            for doc in every:
                ip = self.remoteDB.ipCol.find_one({ '_id': doc['ipId'] })
                cmd = 'REPLACE INTO Switch(IPv4, content) VALUES (\'%s\', \'%s\');' % (ip['ipv4'], str(doc).replace('\'', '"'))
                self.tempDB.execute(cmd)
            self.tempDB.commit()
        elif self.remoteDB.type == 'mysql':
            pass
