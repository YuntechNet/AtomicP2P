from ssh_switch import ssh_switch
from getpass import getpass
from Config import Config
from switch.Switch import Switch


try:
    from pws import host,username,password
except:
    host = input('host: ')
    username = input('username: ')
    password = getpass()

# Test switch  
sw1 = Switch({'host': host, 'username': username, 'password': password})
sw1.initSwitch(operator='system', debug=True)
