from ssh_switch import ssh_switch
from switch.Switch import Switch
import re
import json

command_list = []

def sw_exec(command):
    command_list.append(command)

class script_mode(object):

    def __init__(self,script_file):
        self.script_file = script_file
        self.script = json.load(open(script_file))
        self.command_list = []

    def sw_exec(self,command):
        print(command)

    def script_pre_exec(self,pre_command_code):
        for each in pre_command_code:
            exec(each,globals())


    def script_exlainer(self,command_code):
    
        exec_code =''
        for each in command_code:
            exec_code += each

        exec(exec_code,globals())

        return command_list

    def explain_to_list(self):
        
        self.script_pre_exec(self.script['pre_command'])
        command_list = self.script_exlainer(self.script['command'])
        return command_list
        

