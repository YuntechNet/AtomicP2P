
from network.commands.Command import Command

class ExecuteScript:

    @staticmethod
    def req(redis, cmd):
        Command(redis.name, cmd._to, '--switch execute-script').send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        argv = cmd._command.replace('--switch execute-script', '').split(' ')
        if not cmd._data:
            redis.print('Execute-Script command from %s, responsed' % cmd._from)
            if argv == ['']:
                pass
            else:
                pass
            cmd.swap()
            cmd._data = { 'response': 1 }
            cmd.send(redis)
        else:
            redis.print('Execute-Script feed back from %s, %s' % (cmd._from, cmd._data))
        return None

