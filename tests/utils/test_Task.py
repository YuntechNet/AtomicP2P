import pytest, json

from utils.Task import Task

class TestTask:

    def test_init(self):
        task = Task('Test-A-Redis', 'Test-B-Redis', 'Test')
        assert task._from == 'Test-A-Redis'
        assert task._to == 'Test-B-Redis'
        assert task._content == 'Test'

    def test_parse(self):
        data = json.dumps({ '_from': 'Test-A-Redis', '_to': 'Test-B-Redis', '_content': 'Test' })
        result = Task.parse(data)
        assert result.to() == data
    
    def test_to(self):
        task = Task('Test-A-Redis', 'Test-B-Redis', 'Test')
        assert task.to() == json.dumps({ '_from': 'Test-A-Redis', '_to': 'Test-B-Redis', '_content': 'Test' })
