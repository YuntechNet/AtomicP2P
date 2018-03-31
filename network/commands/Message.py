
from network.commands.Command import Command

class Message:
    
    @staticmethod
    def req(redis, cmd):
        Command(redis.name, cmd._to, 'message', cmd._command.replace('message ', '')).send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        redis.print('Message from %s : %s' % (cmd._from, cmd._data))
        return None
