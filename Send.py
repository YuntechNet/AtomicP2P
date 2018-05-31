import pickle
from Connect import Connect

class Send():
    def __init__(self,Type,Linkip=None,Linkport=0,Linkdata=None):
        self.Type = Type
        self.Linkip = Linkip
        self.Linkport = Linkport
        self.Linkdata = Linkdata

    def sendchoose(self):
        if(self.Type=="command"):
            self.command(self.Linkip,self.Linkport,self.Linkdata)
        
        elif(self.Type=="join"):
            self.JoinNetWork(self.Linkip,self.Linkport,self.Linkdata)

        elif(self.Type=="newlist"):
            self.UploadNewList()

        elif(self.Type=="exit"):
            self.Exit()


    def command(self,linkip,linkport, cmd):
        Sendcmd = Connect(linkip, linkport, 'command', cmd.encode('ascii'))
        Sendcmd.start()

    def JoinNetWork(self,linkip,linkport,imformation):
        if imformation[0]==None:
            imformation[0] = 'no name'
        data = pickle.dumps(imformation)
        Sendcmd = Connect(linkip, linkport, 'join',data)
        Sendcmd.start()
    
    def UploadNewList(self):
        data = pickle.dumps(self.Linkdata)
        for i in range( len(self.Linkdata)):
            Sendcmd = Connect(self.Linkdata[i][1],self.Linkdata[i][2],'newlist',data)
            Sendcmd.start()

    def Exit(self):
        data = b'I leave'
        for i in range( len(self.Linkdata)):
            Sendcmd = Connect(self.Linkdata[i][1],self.Linkdata[i][2], 'message', data)
            Sendcmd.start()