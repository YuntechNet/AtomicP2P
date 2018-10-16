import threading
from threading import Event
from LibreCisco.peer import Peer
from LibreCisco.utils import printText


class Watchdog(threading.Thread):

    def __init__(self,peer,loopDelay=10):
        super(Watchdog, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay
        self.peer=peer
        self.connectlist=peer.connectlist
        self.output_field = peer.output_field

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            for each in self.connectlist:
                addr=each.host[0]
                port=each.host[1]
                mes={'msg':123}
                try:
                    self.peer.sendMessage((addr,port),'message',**mes)
                except IOError:
                    printText("離線")

    def Test(self):
        pass

    def stop(self):
        self.stopped.set()
           
