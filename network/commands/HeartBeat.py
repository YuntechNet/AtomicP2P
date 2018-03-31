
from network.commands.Command import Command

class HeartBeat:

    @staticmethod
    def req(redis, cmd):
        Command(redis.name, cmd._to, 'heart-beat').send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        if not cmd._data:
            redis.print('Heart beat from %s, responsed.' % cmd._from)
            cmd.swap()
            cmd._data = { 'response': 1 }
            cmd.send(redis)
        else:
            redis.print('Heart beat feed back from %s, she is alive.' % cmd._from)
        return None
        
