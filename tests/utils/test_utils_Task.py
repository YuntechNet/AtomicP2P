import pytest, json

from communicate.Command import Command

class TestTask:

    def test_init(self):
        cmd = Command('Test-A-Redis', 'Test-B-Redis', 'Test')
        assert cmd._from == 'Test-A-Redis'
        assert cmd._to == 'Test-B-Redis'
        assert cmd._content == 'Test'

    def test_parse(self):
        data = json.dumps({ '_from': 'Test-A-Redis', '_to': 'Test-B-Redis', '_content': 'Test' })
        result = Command.parse(data)
        assert result.to() == data
    
    def test_to(self):
        cmd = Command('Test-A-Redis', 'Test-B-Redis', 'Test')
        assert cmd.to() == json.dumps({ '_from': 'Test-A-Redis', '_to': 'Test-B-Redis', '_content': 'Test' })
