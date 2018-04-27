from utils.Executor import Executor

class TestExecutor:

    def test_init(self):
        exe = Executor()
        assert exe.sshClient is None
