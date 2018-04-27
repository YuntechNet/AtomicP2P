import json

from ssh_switch import ssh_switch
from getpass import getpass
from Config import Config
from switch.Switch import Switch
from utils.Executor import Executor
#from script_mode import script_mode
from utils.Explainer import ScriptExplainer

try:
    from pws import host,username,password
except:
    host = input('host: ')
    username = input('username: ')
    password = getpass()

# Testing switch  
#sw1 = Switch({'host': host, 'username': username, 'password': password})
#sw1.initSwitch(True)

# Testing send string command
#s = ssh_switch(host=host,username=username,password=password)
#s.login()

#script = script_mode('./test.json')
#command_list = script.explain_to_list()
with open('./schedule/static/test.json') as f:
    jsonContent = json.loads(f.read())
    script = ScriptExplainer(jsonContent)
    command_list = script.explainToList()
    print(command_list)

#exe = Executor(s)

#for each in command_list:
#    (exe, result) = exe._executeStr_(each,short=False)
#    print(result)
ps.logout()
