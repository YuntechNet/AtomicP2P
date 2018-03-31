
import pytest
from subprocess import Popen, PIPE
from queue import Queue

from run import main

class TestRun:

    def test_switchManager(self):
        instance, inputStream, outputStream = main(['--SwitchManager'], debug=True)
        inputStream.execute('exit')

    def test_scheduleManager(self):
        instance, inputStream, outputStream = main(['--ScheduleManager'], debug=True)
        inputStream.execute('exit')

    def test_libServer(self):
        instance, inputStream, outputStream = main(['--LibServer'], debug=True)
        inputStream.execute('exit')

    def test_libCisco(self):
        instance, inputStream, outputStream = main(['--LibCisco'], debug=True)
        inputStream.execute('exit')

    def test_all(self):
        instance, inputStream, outputStream = main([], debug=True)
        inputStream.execute('--switch online')
        inputStream.execute('--switch heart-beat')

        inputStream.execute('--schedule online')
        inputStream.execute('--schedule load-folder')

        inputStream.execute('--libcisco online')
        inputStream.execute('--libcisco heart-beat')

        inputStream.execute('--libserver online')
        inputStream.execute('--libserver heart-beat')
        inputStream.execute('exit')
