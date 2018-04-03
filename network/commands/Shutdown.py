
from network.commands.Command import Command

class Shutdown:

    @staticmethod
    def req(redis, _to, _data=None):
        if _to:
            Command(redis.name, _to, 'shutdown', _data).send(redis)
        else:
            for (key, value) in redis.instance.items():
                value.exit()
        return None

    @staticmethod
    def res(redis, cmd):
        redis.print('Shutdown signal from %s.' % cmd._from)
        for (key, value) in redis.instance.items():
            value.exit()
        return None
        
