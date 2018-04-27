
from utils.User import User
from network.commands.Command import Command

class ExecuteScript:

    @staticmethod
    def req(redis, _to, _data):
        Command(redis.name, _to, '--switch execute-script', _data).send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        argv = cmd._command.replace('--switch execute-script', '').split(' ')
        if not 'response' in cmd._data:
            manager = redis.instance['switchManager']
            redis.print('Execute-Script command from %s, responsed' % cmd._from)
            redis.print('Script content: %s' % cmd._data)
            if argv == ['']:
                pass
            else:
                pass

            for (key, value) in cmd._data.items():
                sw = manager.getDeviceByHost(key)
                if sw:
                    for each in sw:
                        each.stageExecute(User('SwitchManager', 15), value)

            cmd.swap()
            cmd._data = { 'response': 1 }
            cmd.send(redis)
        else:
            redis.print('Execute-Script feed back from %s, %s' % (cmd._from, cmd._data))
        return None

