import datetime

class Peerstatus(object):

    def __init__(self,peer_info):
        self.peer_info = peer_info
        self.lastResponseTime=" "

    

    def __eq__(self, other):
        return self.peer_info == other.peer_info 
    
    def __str__(self):
        return str(self.peer_info)

    def nowTime(self):
        now = datetime.datetime.now()
        self.lastResponseTime = now.strftime("%Y/%m/%d %H:%M:%S")
        return self.lastResponseTime