from ssh_switch import ssh_switch
from getpass import getpass
from Config import Config
from switch.Switch import Switch
import re
import time 
import json

try:
    from pws import host,username,password
except:
    host = input('host: ')
    username = input('username: ')

globals_list = {}

def sw_exec(command):
    print(command)


def script_pre_exec(pre_command_code):
    for each in pre_command_code:
        exec(each,globals())

def script_exec(exec_code):
    exec(exec_code,globals())


def script_exlainer(command_code):
    
    exec_code =''
    for each in command_code:
        exec_code += each
  
    return exec_code

#s= ssh_switch(host=host,username=username,password=password)
#s.login()
script = json.load(open('test00.json'))

script_pre_exec(script['pre_command'])
exec_code = script_exlainer(script['command'])
script_exec(exec_code)
