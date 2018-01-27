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

    def login(self):

        self.ssh=paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.host, port=22, username=self.username,password=self.password,
                    look_for_keys=False, allow_agent=False)
                
        self.shell = self.ssh.invoke_shell() #need to setting termial size...etc

    def send_command(self,command):
        
        self.shell.send(str(command)+'\n')
        time.sleep(.5)
        output = self.shell.recv(65535)
        return output


