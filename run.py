from ssh_switch import ssh_switch
from getpass import getpass
from command import basic_command
from Executor import Executor
from Explainer import Explainer

try:
    from pws import host,username,password
except:
    host = input('host: ')
    username = input('username: ')
    password = getpass()

s = ssh_switch(host=host,username=username,password=password)
s.login()

#cmd = ['enable', 'conf ter', 'exit', 'show interface', 'disable', 'exit']
cmd = ['show run', 'conf t', 'exit']
exp = Explainer()
exe = Executor(s)

for each in cmd:
    cmdInstance = exp._explain_(each)
    executed = exe._execute_(cmdInstance, short=False)
    exe = executed[0]
    print(executed[1])

##interactive_mode(s)
#b = basic_command(connection=s,switch_mode=1)
##out = b.parse_interface_status()
#out = b.configure_terminal()

#print(out)
#out= b.interface_Ethernet('Fa0/2')
#print(out)


#def interactive_mode(connection):
#
#    while True:
#        command = input('command: ')
#        result = s.send_command(command)
#        print(result.decode('UTF-8'))
