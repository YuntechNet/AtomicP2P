import pytest, json

from network.Command import Command, Online, HeartBeat, Shutdown, Commander
from network.Manager import RedisManager

class TestCommand:

    def test_init(self):
        c = Command('A', 'B', 'Test')
        assert c._from == 'A'
        assert c._to == 'B'
        assert c._command == 'Test'
    
    def test_parse(self, mocker):
        c = Command.parse(json.dumps({'_from': 'A', '_to': 'B', '_command': 'Test', '_data': None}))
        assert c._from == 'A'
        assert c._to == 'B'
        assert c._command == 'Test'

    def test_to(self):
        j = json.dumps({'_from': 'A', '_to': 'B', '_command': 'Test', '_data': None})
        jStr = Command('A', 'B', 'Test').to()
        assert jStr == j
        
    @pytest.mark.skip('L19:Seaking mock.')
    def test_send(self, mocker):
        c = Command('A', 'B', 'Test')
        mMethod = mocker.patch.object(c, 'send')
        c.send(None)
        assert mMethod.called

    def test_swap(self):
        c = Command('A', 'B', 'Test')
        c.swap()
        assert c._from == 'B'
        assert c._to == 'A'

@pytest.mark.skip('Wait for further edit.')
class TestOnline:

    def test_init(self):
        c = Online(Command('A', 'B', 'Test'))
        assert c._from == 'A'
        assert c._to == 'B'
        assert c._command == 'Test'

    def test_req(self):
        c = Online(Command('A', 'B', 'Test'))
        assert c.req() == c
        
    def test_res(self):
        c = Online(Command('A', 'B', 'Test'))
        c.res(None)
        assert c._from == 'B'
        assert c._to == 'A'
        assert c._command == 'I\'m online bitch!'

@pytest.mark.skip('Wait for further edit.')
class TestHeartBeat:

    def test_init(self):
        c = HeartBeat(Command('A', 'B', 'Test'))
        assert c._from == 'A'
        assert c._to == 'B'
        assert c._command == 'Test'

    def test_req(self):
        c = HeartBeat(Command('A', 'B', 'Test'))
        assert c.req() == c
        
    @pytest.mark.skip('L48-51:Seaking mock.')
    def test_res(self):
        c = HeartBeat(Command('A', 'B', 'Test'))
        c.res(None)
        assert c._from == 'B'
        assert c._to == 'A'
        assert c._command == 'I\'m online bitch!'

@pytest.mark.skip('Wait for further edit.')
class TestShutdown:

    def test_init(self):
        c = Shutdown(Command('A', 'B', 'Test'))
        assert c._from == 'A'
        assert c._to == 'B'
        assert c._command == 'Test'

    def test_req(self):
        c = Shutdown(Command('A', 'B', 'Test'))
        assert c.req() == c
            
    def test_res(self):
        c = Shutdown(Command('A', 'B', 'Test'))
        assert c.res(None) == c

class TestCommander:

    def test_init(self):
        c = Commander(None)
        assert c.INS == None

    @pytest.mark.skip('L70-78:Seaking mock.')
    def test_process(self):
        pass

    @pytest.mark.skip('L82-93:Seaking mock.')
    def test_processReq(self):
        pass
