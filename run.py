from Server import Server
from Client import Client
import sys

def main():
    if len(sys.argv) >= 5:
        s = Server(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])      
    elif ( len(sys.argv) >= 3 and len(sys.argv) < 5):
        s = Server(sys.argv[1], sys.argv[2], "", "")
    s.start()   

    while True:
        cmd = input('imput what do you want to do:')
        if cmd=='help':
            print('S: send your message to aim.')
        elif cmd == 'S':
            ip = str(input ('what the host do you want to send:'))
            pt = int(input ('what the port do you use:'))
            cmd = input('imput is your command:')
            print('I send to',ip,pt)
            Sendcmd = Client(ip, pt, 'command', cmd)
            Sendcmd.start()


if __name__ == '__main__' :
    main()