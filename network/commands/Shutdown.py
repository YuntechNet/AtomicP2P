
from network.commands.Command import Command

class Shutdown:

    @staticmethod
    def req(redis, cmd):
        Command(redis.name, cmd._to, 'shutdown').send(redis)
        return None

    @staticmethod
    def res(INS, cmd):
        INS.redis.print('Shutdown signal from %s.' % cmd._from)
        return None
        