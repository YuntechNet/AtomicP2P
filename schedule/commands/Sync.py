
from network.commands.Command import Command

class Sync:

    @staticmethod
    def req(redis, _to, _data=None):
        Command(redis.name, _to, '--schedule sync', _data).send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        if not cmd._data:
            manager = redis.instance['scheduleManager']
            redis.print('Sync command from %s, responsed' % cmd._from)
            manager.toSystem()
            cmd._data = { 'response': 1 }
            cmd.swap()
            cmd.send(redis)
        else:
            redis.print('Sync feed back from %s, %s' % (cmd._from, cmd._data))
        return None
