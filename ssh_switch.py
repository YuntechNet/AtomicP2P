import paramiko
import time

class ssh_switch(object):

    def __init__(self,host='',username='',password='',port=22, timeout=60):
        self.host=host
        self.username=username
        self.password=password
        self.port=port
        self.timeout = timeout
        self.ssh = None
        self.shell = None
        self.output = None

    def login(self, timeout=None):
        self.timeout = timeout if timeout is not None else self.timeout
        self.ssh=paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.host, port=22, username=self.username,password=self.password, timeout=self.timeout, look_for_keys=False, allow_agent=False)
                
        self.shell = self.ssh.invoke_shell() # need to setting termial size...etc
        self.output = self.shell.recv(65535)
        return self

    def logout(self):
        if self.ssh:
            self.ssh.close()

    def sendCommand(self, command, wrap=True):
        self.shell.send(str(command) + ('\n' if wrap else ''))

    def send_command(self, command, wrap=True, time_sleep=.5, debug=False):
        self.sendCommand(command, wrap)
        time.sleep(time_sleep)
        self.output = self.shell.recv(65535).decode('utf-8')

        if debug:
            print(self.output)
        return self.output
    
    def isActive(self):
        return self.ssh.get_transport().is_active()
