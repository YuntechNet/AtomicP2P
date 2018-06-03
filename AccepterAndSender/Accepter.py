import pickle
class Accepter():
    def __init__(self, Peer, Type, Data, conn, addr):
        self.type = Type
        self.data = Data
        self.peer = Peer
        self.conn = conn
        self.addr = addr
        self.error = False
    def typechoose(self):
        self.conn.send(b"server received your message.")
        if self.type=='newlist':
            return self.AcceptNewList()
        elif self.type=='join':
            return self.AcceptNewJoin()
        else:          
            self.ElseAccept()
            return ['nothing']

    def AcceptNewList(self):
        savelistbuffer=[]
        datalist = pickle.loads(self.data)
        for member in datalist:
            jmp=False
            for mydata in self.peer.connectlist:
                if mydata==member:
                    jmp=True
                    break 
            if jmp==True:
                continue
            self.ErrorCheck(member[1],member[2]) 
            savelistbuffer.insert(0,member)

        print("server get:", savelistbuffer)           
        savebuffer=['new list',savelistbuffer]
        return savebuffer

    def AcceptNewJoin(self):
        savelistbuffer = pickle.loads(self.data)
        savelistbuffer.insert(1,self.addr[0])

        self.ErrorCheck(savelistbuffer[1],savelistbuffer[2])
        if self.error==False:
            print ("server get:", savelistbuffer)
            print("server say: a peer join")
        savebuffer = ['new list',savelistbuffer]
        return self.GoodConnect(savebuffer)

    def ElseAccept(self):
        data = self.data.decode('ascii')
        print ("server get:", data)
        self.GoodConnect()

    def ErrorCheck(self, IP, port):
        if(len(IP)<7 or len(IP)>15 or port>65535 or port<0):
            self.error=True
        
    def GoodConnect(self, buffer=None):
        if self.error==True:
            buffer=['error data']
            self.conn.send(b"There are some error, so I can accept it.")
        else :
            self.conn.send(b"This is a good connection")
        return buffer