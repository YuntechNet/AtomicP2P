
from network.commands.Command import Command

class Online:

    @staticmethod
    def req(redis, _to, _data=None):
        Command(redis.name, _to, 'online', _data).send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        redis.print('%s is online' % cmd._from)
        return None
