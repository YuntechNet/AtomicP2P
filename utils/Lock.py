# Lock
#   Class definition for switch execute flow control.
#   Prevent other user to interact with same switch cause unpredictable error.
#
class Lock:

    def __init__(self, initState=False):
        self.lock = initState
        self.locker = None

    def setLock(self, locker):
        self.lock = True
        self.locker = locker

    def unLock(self):
        self.lock = False
        self.locker = None

    def isLock(self):
        return self.lock

    def getLocker(self):
        return self.locker

