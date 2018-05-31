import pickle

class Handle:
    def __init__(self, Peer, Type, Data, conn, addr):
        self.Type = Type
        self.Data = Data
        self.Peer = Peer
        self.conn = conn
        self.addr = addr

    def typechoose(self):
        if(self.Type=='newlist'):
            self.AcceptNewList()

        elif (self.Type=='join'):
            self.AcceptNewJoin()

        else:          
            self.ElseAccept()

    def AcceptNewList(self):
        datalist = pickle.loads(self.Data)
        for data in datalist:
            jmp=False
            for mydata in self.Peer.connectlist:
                if mydata==data:
                    jmp=True
                    break 
            if jmp==True:
                continue
            self.Peer.connectlist.insert(0,data)
        print("server get:", self.Peer.connectlist)   
        self.conn.send(b"the server say: server received you message.")

    def AcceptNewJoin(self):
        datalist = pickle.loads(self.Data)
        self.conn.send(b"the server say: server received you message.")
        print ("server get:", datalist)

        self.Peer.connectlist.insert( 0, (datalist[0],self.addr[0],datalist[1]) )
        self.Peer.Sendmessage("Newlist", None, 0, self.Peer.connectlist)
        print("server say: a peer join")

    def ElseAccept(self):
        data = self.Data.decode('ascii')
        self.conn.send(b"the server say: server received you message.")
        print ("server get:", data)