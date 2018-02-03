import paramiko
import time

class ssh_switch(object):

    def __init__(self,host='',username='',password='',port=22):
        self.host=host
        self.username=username
        self.password=password
        self.port=port
        self.ssh = None
        self.shell = None
        self.output = None

    def login(self):

        self.ssh=paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.host, port=22, username=self.username,password=self.password,look_for_keys=False, allow_agent=False)
                
        self.shell = self.ssh.invoke_shell() #need to setting termial size...etc
        self.output = self.shell.recv(65535)
        return self

    def send_command(self,command,wrap=True,time_sleep=.5):

        if wrap:
            command = str(command)+'\n'
        else:
            command = str(command)
        self.shell.send(command)
        time.sleep(time_sleep)
        self.output = self.shell.recv(65535)
        return self.output.decode('utf-8')
        

