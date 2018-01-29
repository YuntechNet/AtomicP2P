from ssh_switch import ssh_switch


class basic_command(object):

    def __init__(self,connection): 
        self.con = connection

    def en(self):
        return self.con.send_command('en') 

    

