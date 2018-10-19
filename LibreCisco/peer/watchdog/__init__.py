
from LibreCisco.utils.manager import ThreadManager
from LibreCisco.utils import printText


class Watchdog(ThreadManager):

    def __init__(self,peer,loopDelay=10):
        super(Watchdog, self).__init__(loopDelay=loopDelay,
                                   output_field=peer.output_field,
                                   auto_register=True)
        
        self.peer=peer
        self.connectlist=peer.connectlist
        

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            for each in self.connectlist:
                addr=each.host[0]
                port=each.host[1]
                mes={'msg':123}
                try:
                    # self.peer.sendMessage((addr,port),'message',**mes)
                    pass
                except IOError:
                    printText("離線")

    def Test(self):
        pass

    def stop(self):
        self.stopped.set()

    def registerHandler(self):
        self.handler = {
            
        }

    def registerCommand(self):
        self.commands = {
          
        }

    def onProcess(self, msg_arr, **kwargs):
        
        return ''
           
