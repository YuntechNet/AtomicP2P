import paramiko
from getpass import getpass
import time

ip = input('ip: ')
username = input('username: ')
password = getpass()

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, port=22, username=username,  
                        password=password,
                        look_for_keys=False, allow_agent=False)

shell = ssh.invoke_shell()
output = shell.recv(65535)
print (output)

while True:	
    command = input('command: ')
    shell.send(str(command)+'\n')
    time.sleep(.5)
    output = shell.recv(65535)
    print(output.decode('UTF-8'))


