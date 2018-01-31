from ssh_switch import ssh_switch
from getpass import getpass
from command import basic_command
try:
    from pws import host,username,password
except:
    host = input('host: ')
    username = input('username: ')
    password = getpass()

def interactive_mode(connection):

    while True:
        command = input('command: ')
        result = s.send_command(command)
        print(result.decode('UTF-8'))

s = ssh_switch(host=host,username=username,password=password)
s.login()
#interactive_mode(s)
b = basic_command(connection=s,switch_mode=1)
#out = b.parse_interface_status()
out = b.configure_terminal()

print(out)
out= b.interface_Ethernet('Fa0/2')
print(out)
