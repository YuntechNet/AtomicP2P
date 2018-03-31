
from network.commands.Command import Command

class Shutdown:

    @staticmethod
    def req(redis, _to, _data=None):
        Command(redis.name, _to, 'shutdown', _data).send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        redis.print('Shutdown signal from %s.' % cmd._from)
        return None
        
