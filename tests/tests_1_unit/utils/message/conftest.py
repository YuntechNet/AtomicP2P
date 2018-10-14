import pytest

from LibreCisco.utils.message import Message, Handler

@pytest.fixture(scope='class')
def message():
    return Message(_host=('0.0.0.0', 9000), _type='a', _data='test text')

@pytest.fixture(scope='class')
def handler():
    return Handler(None)
