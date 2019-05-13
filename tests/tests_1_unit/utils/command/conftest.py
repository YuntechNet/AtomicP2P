
import pytest
from LibreCisco.utils.command import Command


@pytest.fixture(scope='class')
def command():
    return Command(None)
