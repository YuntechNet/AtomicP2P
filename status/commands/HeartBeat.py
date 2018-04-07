import logging

from network.commands.Command import Command

class HeartBeat:

    @staticmethod
    def req(redis, _to, _data=None):
        Command(redis.name, _to, 'heart-beat', _data).send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        redis.instance['statusManager'].markStatus(cmd._from, True)
        if not cmd._data:
            redis.print('Heart beat from %s, responsed.' % cmd._from, logging.DEBUG)
            cmd.swap()
            cmd._data = { 'response': 1 }
            cmd.send(redis)
        else:
            redis.print('Heart beat feed back from %s, she is alive.' % cmd._from, logging.DEBUG)
        return None
        
