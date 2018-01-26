from pexpect import ExceptionPexpect

class OExceptionPexpect(ExceptionPexpect):

    def __init__(self, value):
        super().__init__(value)
