from getpass import getpass
from ssh_class import ssh_switch
from command_class import EnMode



def interactive_mode(connection):
    while True:
        command = input('command: ')
        result = connector.send_command(command)
        print(result)
        
host = input('host: ')
username = input('username: ')
print('password: ')
password = getpass()
connector = ssh_switch(host=host,username=username,password=password)
connector.login()
interactive_mode(connector)

#instruction_Mode
#EnConnector = EnMode(connection=connector,switch_mode=1)
#out = b.parse_interface_status()
#out = EnConnector.configure_terminal()

#print(out)
#out= EnConnector.interface_Ethernet('Fa0/2')
#print(out)
