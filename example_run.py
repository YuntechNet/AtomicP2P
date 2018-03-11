from ssh_switch import ssh_switch
from getpass import getpass
from utils.Executor import Executor
from utils.Explainer import Explainer

try:
    from pws import host,username,password
except:
    host = input('host: ')
    username = input('username: ')
    password = getpass()

s = ssh_switch(host=host,username=username,password=password)
s.login()

cmd = ['show run','conf t','hostname test001' ,'exit']
exp = Explainer()
exe = Executor(s)
exe._mode_()

for each in cmd:
    cmdInstance = exp._explain_(each)
    (exe, result) = exe._execute_(cmdInstance, short=False)
    if result == '':
        break
    print(result)

