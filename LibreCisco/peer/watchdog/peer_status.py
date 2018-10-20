

class Peerstatus(object):

    def __init__(self,peer_info):
        self.peer_info = peer_info

    def __eq__(self, other):
        return self.peer_info == other.peer_info 
    
    def __str__(self):
        return str(self.peer_info)