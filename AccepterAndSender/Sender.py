import pickle
import sys
sys.path.append('..')
from PeerLink.PeerConnection import PeerConnection

class Sender():
    def __init__(self,Type,Linkip=None,Linkport=0,Linkdata=None):
        self.Type = Type
        self.Linkip = Linkip
        self.Linkport = Linkport
        self.Linkdata = Linkdata

    def SendChoose(self):
        if(self.Type=="command"):
            self.Command(self.Linkip,self.Linkport,self.Linkdata)
        
        elif(self.Type=="join"):
            self.JoinNetWork(self.Linkip,self.Linkport,self.Linkdata)

        elif(self.Type=="newlist"):
            self.UploadNewList()

        elif(self.Type=="exit"):
            self.Exit()

    def Command(self,linkip,linkport, cmd):
        Sendcmd = PeerConnection(linkip, linkport, 'command', cmd.encode('ascii'))
        Sendcmd.start()

    def JoinNetWork(self,linkip,linkport,imformation):
        if imformation[0]==None:
            imformation[0] = 'no name'
        data = pickle.dumps(imformation)
        Sendcmd = PeerConnection(linkip, linkport, 'join',data)
        Sendcmd.start()
    
    def UploadNewList(self):
        data = pickle.dumps(self.Linkdata)
        for i in range( len(self.Linkdata)):
            Sendcmd = PeerConnection(self.Linkdata[i][1],self.Linkdata[i][2],'newlist',data)
            Sendcmd.start()

    def Exit(self):
        data = b'I leave'
        for i in range( len(self.Linkdata)):
            Sendcmd = PeerConnection(self.Linkdata[i][1],self.Linkdata[i][2], 'message', data)
            Sendcmd.start()