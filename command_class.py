import re 
    
class EnMode(object):

    def __init__(self,connection=None,switch_mode=0): 
        self.con = connection
        self.switch_mode = switch_mode
        #0 = user, 1 = Privileged/EnMode ,2 = Global Configuration,3 = Interface Configuration

    #Shorthand
    def send(self,command,wrap=True):
        return self.con.send_command(command,wrap)
    
    #press more to get all informationr 
    def more(self,result_tmp):

        result = result_tmp
           
        while re.search('ore--',str(result_tmp)):
            result_tmp = self.send(' ',wrap=False)
            result = result + result_tmp 
        return result
    
    def enable(self):
        if(self.switch_mode==0):
            self.switch_mode = 1 #enter Privileged 
            return self.send('enable')
        else:
            raise Exception("switch mode not correct,now mode : "+str(self.switch_mode))

    def configure_terminal(self):
        if(self.switch_mode==1):
            self.switch_mode = 2 #Global Configuration
            return self.send('configure terminal')
        else:
            raise Exception("switch mode not correct,now mode : "+str(self.switch_mode))

    def config_interface(self,interface):
        if(self.switch_mode==2):
            command = 'interface '+ interface
            return self.send(command)
        else:
            raise Exception("switch mode not correct,now mode : "+str(self.switch_mode))

    #need rearrange   
    def parse_interface_status(self):
        interface = {}
        interface_detail = self.show_interfaces_status()
        interface_detail = interface_detail.split('\r\n')

        for each in interface_detail:

            if re.match('.*/',each):
                tmp = each.split()
                ethernet = tmp[0]

                for data in tmp:
                    if re.search('connect',data):
                        status = data 

                    if re.search(r'^[\d]+$',data): 
                        vlan = data

                interface[ethernet] = {'status':status,'vlan':vlan}

        return interface

    '''
    show function
    '''
    def show (self,command):

        if self.switch_mode ==1:
        
            result_tmp = self.send('show '+command)
            result = self.more(result_tmp)    
            return result 
        else:
            raise Exception("switch mode not correct,now mode : "+str(self.switch_mode))

    def show_interfaces(self):
        #get all information
        return self.show('interfaces')

    def show_interfaces_status(self):
        return self.show('interfaces status')
