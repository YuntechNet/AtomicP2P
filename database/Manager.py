import threading
from threading import Event

from database.Database import RemoteDatabase

# RemoteDBManager
#   A thread in SwitchManager for communicate with local database.
#
class RemoteDBManager(threading.Thread):

    def __init__(self, msgQueue, tempDB, config, sleep=300):
        threading.Thread.__init__(self)
        self.msgQueue = msgQueue
        self.stopped = Event()
        self.sleep = sleep

        self.tempDB = tempDB
        self.remoteDB = RemoteDatabase(self.msgQueue, config)

    def print(self, msg):
        self.msgQueue.put('[RemoteDBManager] %s' % msg)

    def run(self): # Override
        while not self.stopped.wait(self.sleep):
            self.syncToLocal()

    def syncToLocal(self):
        self.print('Loading devices.')
        if self.remoteDB.type == 'mongodb':
            from bson.json_util import dumps as bsonDumps
            every = self.remoteDB.switchCol.find({})
            for doc in every:
                ip = self.remoteDB.ipCol.find_one({ '_id': doc['ipId'] })
                cmd = 'REPLACE INTO Switch(IPv4, content) VALUES (\'%s\', \'%s\');' % (ip['ipv4'], bsonDumps(doc))
                self.tempDB.execute(cmd)
            self.tempDB.commit()
        elif self.remoteDB.type == 'mysql':
            pass
