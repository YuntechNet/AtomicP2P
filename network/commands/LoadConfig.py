
from network.commands.Command import Command

class LoadConfig:

    @staticmethod
    def req(redis, _to, _data=None):
        Command(redis.name, _to, 'load-config', _data).send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        if not cmd._data:
            manager = redis.instance
            redis.print(cmd)
            cmd._data = { 'response': 1 }
            for (key, value) in manager.items():
                value.loadConfig()
            cmd.swap()
            cmd.send(redis)
        else:
            redis.print('Load config feed back from %s, %s' % (cmd._from, cmd._data))
        return None
