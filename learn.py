from ssh_switch import ssh_switch
from getpass import getpass
from Config import Config
from switch.Switch import Switch
import re
import time 

try:
    from pws import host,username,password
except:
    host = input('host: ')
    username = input('username: ')


def loop_letter():
    letter = []
    for i in range(ord('a'),ord('z')+1):
        letter.append(chr(i))
    return letter

def next_letter(previous_letter):
    return chr(ord(previous_letter)+1)



class model(object):

    def __init__(self,sshClient,time_sleep):
        self.sshClient = sshClient
        self.time_sleep = time_sleep
        self.hostname = self.get_hostname()

    def clr(self):
        self.sshClient.sendCommand('\x17',wrap=False)

    def check_command(self,string,space=True):

        if space:
            output = self.sshClient.send_command(string+' \t',time_sleep=self.time_sleep,wrap=False)
        else :
            output = self.sshClient.send_command(string+'\t',time_sleep=self.time_sleep,wrap=False)
        self.clr()
        return output

    def get_command(self,string):
        output = self.sshClient.send_command(string+'?',time_sleep=self.time_sleep,wrap=False)
        return output

    def get_args(self,string,short=False):
        self.clr()
        result = self.sshClient.send_command(string+" ?",time_sleep=self.time_sleep,wrap=False)   
        while('#' not in result and '>' not in result):
            if ' --More--' in result:
                result = result.replace(' --More-- ', '') + self.sshClient.send_command('q' if short else ' ', wrap=False)
            else:
                break

        self.clr()
        return result

    def get_hostname(self,get_model=True):

        self.clr()
        output = self.sshClient.send_command('')
        if get_model :
            pass
        else:
            if '#' in output:
                output =  output.replace('#','')
            elif '>' in output:
                output = output.replace('>','')

        hostname = output.replace('\r\n','').replace('\x08','').strip() 
        return hostname

    def get_match(self,command):

        match_list = [command]
        self.clr()
        for i in range(len(command)-1,0,-1):
            self.clr()
            print('##############################################################')
            print(command)
            out =  sshClient.send_command(command[0:i]+'\t',wrap=False).replace(self.hostname,'').replace('\x08','').replace('\x07','').replace('\r','').strip().split('\n')
            if out[1] == command:
                print()
            print(out)
            self.clr()
            print('#############################################################')
        return match_list


def crawl_command(sshClient,time_sleep=1):

    start_time = time.time()
    
    _model = model(sshClient=sshClient,time_sleep=time_sleep)

    result =  {}
    Ambiguous = {}
    nothing = {}
    command = {}

    letter_list = loop_letter()
    hostname = _model.get_hostname()
    for letter in letter_list:
        output = _model.check_command(letter)
        if re.search('Ambiguous',output):
            Ambiguous[letter]= output
            result[letter] = _model.get_command(letter).replace(letter+'?','').replace(hostname+letter,'').replace('\x08','').split()

        elif re.search(hostname+letter+' ',output):
            nothing[letter] = output

        elif re.search(hostname+letter,output):
            command[letter] = [output.split('\n')[1].replace(hostname,'').strip()]

    end_time = time.time()
    print(end_time-start_time)
    result.update(command)

    return sshClient,result,nothing
   

def crawl_command_L2(sshClient,dict_command,time_sleep=1):

    _model = model(sshClient,time_sleep=time_sleep)

    hostname = _model.get_hostname()

    for letter in dict_command:

        command_list = []

        for each_command in dict_command[letter]:
            a = _model.get_match(each_command)

            command_dict = {}
            out = _model.get_args(each_command).replace(hostname+each_command,'').replace(each_command+' ?','').replace(hostname,'').replace('\x08','').split('\n')
    
            args_list = []

            for each in out:
                if  re.search(r'\w',each) :
                    if not re.match('<cr>',each.split()[0]): 
                        args_list.append(each.split()[0]) 

            command_dict[each_command] = {'args':args_list}

            #print(command_dict)
            command_list.append(command_dict)
        dict_command[letter] = command_list

    return dict_command
s = ssh_switch(host=host,username=username,password=password)
s.login()

sshClient,result,nothing = crawl_command(s)


#print(result)
out = crawl_command_L2(sshClient,result)
#print(out)
