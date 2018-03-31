
from network.commands.Command import Command

class Online:

    @staticmethod
    def req(redis, cmd):
        Command(redis.name, cmd._to, 'online').send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        redis.print('%s is online' % cmd._from)
        return None
