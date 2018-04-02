
from network.commands.Command import Command

class Stop:

    @staticmethod
    def req(redis, _to, _data=None):
        Command(redis.name, _to, '--schedule stop', _data).send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        argv = cmd._command.replace('stop', '').split(' ')
        if not cmd._data:
            manager = redis.instance['scheduleManager']
            redis.print('Stop cmd from %s, responsed' % cmd._from)
            if argv == ['']:
                [ value.exit() for (key, value) in manager.schedules.items() ]
                manager.schedules.clear()
            else:
                [ value.exit() for (key, value) in manager.schedules.copy().items() if key in argv ]
            cmd.swap()
            cmd._data = { 'response': 1 }
            cmd.send(redis)
        else:
            redis.print('Stop cmd feed back from %s.' % cmd._from)
        return None
