
from network.commands.Command import Command

class Start:

    @staticmethod
    def req(redis, _to, _data=None):
        Command(redis.name, _to, '--schedule start', _data).send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        argv = cmd._command.replace('--schedule start', '').split(' ')
        if not cmd._data:
            manager = redis.instance['scheduleManager']
            redis.print('Start cmd from %s, responsed' % cmd._from)
            if argv == ['']:
                [ value.start() for (key, value) in manager.schedules.items() ]
            else:
                [ value.start() for (key, value) in manager.schedules.items() if key in argv ]
            cmd.swap()
            cmd._data = { 'response': 1 }
            cmd.send(redis)
        else:
            redis.print('Start cmd feed back from %s.' % cmd._from)
        return None
