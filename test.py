from ssh_switch import ssh_switch
from getpass import getpass
from Config import Config
from switch.Switch import Switch
from utils.Executor import Executor


try:
    from pws import host,username,password
except:
    host = input('host: ')
    username = input('username: ')
    password = getpass()

# Testing switch  
#sw1 = Switch({'host': host, 'username': username, 'password': password})
#sw1.initSwitch(operator='system', debug=True)

# Testing send string command
s = ssh_switch(host=host,username=username,password=password)
s.login()

cmd = ['show run','conf t','hostname test001' ,'exit']
exe = Executor(s)
exe._mode_()

(exe, result) = exe._executeStr_('show run', short=False)
s.logout()
print(result)
