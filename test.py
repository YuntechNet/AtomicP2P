from ssh_switch import ssh_switch
from getpass import getpass
from Config import Config
from switch.Switch import Switch
from utils.Executor import Executor
from script_mode import ScriptExplainer,FormatExplainer
import json

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
#s = ssh_switch(host=host,username=username,password=password)
#s.login()

script = FormatExplainer('./demo/script_demo')
script.dataLoad(json.load(open('./demo/TestIpTable.json')))
script.dataLoad(json.load(open('./demo/TestSwitchObjectId.json')))
script.parseScript()
print(script.explainToList())

#exe = Executor(s)

#for each in command_list:
#    (exe, result) = exe._executeStr_(each,short=False)
#    print(result)
#s.logout()
