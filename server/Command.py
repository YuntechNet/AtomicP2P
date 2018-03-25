from communicate.Command import Command, Commander

class LibServerCommand(Commander):

    def __init__(self, instance):
        Commander.__init__(self, instance)

    def process(self, command):
        if not super(LibServerCommand, self).process(command):
            pass
        else:
            self.INS.redis.print('message from %s: %s' % (command._from, command._content))

    @staticmethod
    def processReq(redis, command):
        if not Commander.processReq(redis, command):
            pass
        return False
