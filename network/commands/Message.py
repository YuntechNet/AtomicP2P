
from network.commands.Command import Command

class Message:
    
    @staticmethod
    def req(redis, _to, _data):
        if _to:
            Command(redis.name, _to, 'message', _data).send(redis)
        else:
            redis.print('You need to specify a process to send.')
        return None

    @staticmethod
    def res(redis, cmd):
        redis.print('Message from %s : %s' % (cmd._from, cmd._data))
        return None
