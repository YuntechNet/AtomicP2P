import logging, threading, redis

from utils.Manager import ThreadManager
from database.Database import TempDatabase, RemoteDatabase

# DatabaseManager
#   A thread in each manager for communication with local and remote database.
#
class DatabaseManager(ThreadManager):

    def __init__(self, outputQueue, config, sleep=300):
        ThreadManager.__init__(self, 'DatabaseManager', outputQueue)
        self.sleep = sleep

        if 'TEMP_DATABASE' in config:
            self.temporDB = TempDatabase(outputQueue, config['TEMP_DATABASE'])
        if 'DATABASE' in config:
            self.remoteDB = RemoteDatabase(outputQueue, config['DATABASE'])
        self.print('inited.', logging.INFO)

    def run(self):
        while not self.stopped.wait(self.sleep):
            self.sync()

    def sync(self):
        raise NotImplementedError
       
