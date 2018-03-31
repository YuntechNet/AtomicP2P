
from network.commands.Command import Command

class Message:
    
    @staticmethod
    def req(redis, _to, _data):
        Command(redis.name, _to, 'message', _data).send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        redis.print('Message from %s : %s' % (cmd._from, cmd._data))
        return None
