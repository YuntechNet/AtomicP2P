
from network.commands.Command import Command

class Online:

    @staticmethod
    def req(redis, _to, _data=None):
        if _to:
            Command(redis.name, _to, 'online', _data).send(redis)
        else:
            redis.print('You need to specify a process to send.')
        return None

    @staticmethod
    def res(redis, cmd):
        redis.print('%s is online' % cmd._from)
        return None
