from ssh_switch import ssh_switch
import re 
    
class basic_command(object):

    def __init__(self,connection=None,switch_mode=0): 
        self.con = connection
        self.switch_mode = switch_mode
        #0 = user, 1 = Privileged ,2 = Global Configuration,3 = Interface Configuration

    #Shorthand
    def send(self,command,wrap=True):
        return self.con.send_command(command,wrap)
    
    def more(self):
        pass
        

    def enable(self):
        self.switch_mode = 1 #enter Privileged 
        return self.send('enable')
    
    def show_interface(self):
        #get all information
        if self.switch_mode ==1:
        
            result_tmp = self.send('show interface')
            result = result_tmp
            pattern = re.compile('ore--')
           
           
            while pattern.search(str(result_tmp)):
                result_tmp = self.send(' ',wrap=False)
                result = result + result_tmp 

            return result 
        else:
            raise Exception("switch mode not correct,now mode : "+str(self.switch_mode))

    def configure_terminal(self):
        self.switch_mode = 2 #Global Configuration
        return self.send('configure terminal')

    def interface_Ethernet(self,Ethernet,port):
        command = 'interface'
        
#Todo switch mode status
