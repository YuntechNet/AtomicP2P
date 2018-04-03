
from network.commands.Command import Command

class LoadConfig:

    @staticmethod
    def req(redis, _to, _data=None):
        if _to:
            Command(redis.name, _to, 'load-config', _data).send(redis)
        else:
            for (key, value) in redis.instance.items():
                value.loadConfig()
        return None

    @staticmethod
    def res(redis, cmd):
        if not cmd._data:
            cmd._data = { 'response': 1 }
            for (key, value) in redis.instance.items():
                value.loadConfig()
            cmd.swap()
            cmd.send(redis)
        else:
            redis.print('Load config feed back from %s, %s' % (cmd._from, cmd._data))
        return None
