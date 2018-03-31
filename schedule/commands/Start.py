
from network.commands.Command import Command

class Start:

    @staticmethod
    def req(redis, cmd):
        Command(redis.name, cmd._to, '--schedule start').send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        argv = cmd._command.replace('start', '').split(' ')
        if not cmd._data:
            redis.print('Start cmd from %s, responsed' % cmd._from)
            if argv == ['']:
                [ value.start() for (key, value) in redis.manager.schedules.items() ]
            else:
                [ value.start() for (key, value) in redis.manager.schedules.items() if key in argv ]
            cmd.swap()
            cmd._data = { 'response': 1 }
            cmd.send(redis)
        else:
            redis.print('Start cmd feed back from %s.' % cmd._from)
        return None
