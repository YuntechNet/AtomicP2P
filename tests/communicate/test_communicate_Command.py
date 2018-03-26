
from communicate.Command import Command, Online, HeartBeat, Shutdown, Commander

class TestCommand:

    def test_init(self):
        c = Command('A', 'B', 'Test Content')
        assert c._from == 'A'
        assert c._to == 'B'
        assert c._content == 'Test Content'
        
        c.swap()
        assert c._from == 'B'
        assert c._to == 'A'
        
class TestOnline:

    def test_init(self):
        c = Online(Command('A', 'B', 'Content'))

class TestHeartBeat:

    def test_init(self):
        c = HeartBeat(Command('A', 'B', 'Content'))

class TestShutdown:

    def test_init(self):
        c = Shutdown(Command('A', 'B', 'Content'))

