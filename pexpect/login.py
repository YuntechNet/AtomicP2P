import pexpect
import getpass 
#import sys

class connection(object):

    def __init__(self,ip='',userName='',password='',port=22,sha1=True):
        self.ip =ip
        self.userName=userName
        self.password=password
        self.port =port
        self.sha1=sha1

    def login(self):
        command ='ssh -p '+port+" "+userName+'@'+ip
        sha1_parameter = "KexAlgorithms=+diffie-hellman-group1-sha1"
        if(self.sha1):
            command = command +' -o '+sha1_parameter
        connection = pexpect.spawn(command)
        connection.timeout = 4
        connection.expect("(?i)Password:")

        output = connection.sendline(self.password)
        print(output)
        output=connection.expect('#')

        print(output)
        
        return connection

ip = input('ip: ')
userName=input('userName: ')
password=getpass.getpass()
port=input('port: ')


s = connection(ip=ip,userName=userName,password=password)
s.login()
