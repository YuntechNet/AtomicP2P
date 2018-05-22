from Server import Server
from Client import Client
import sys

def main(argv):
    if len(sys.argv) < 2:
        print (sys.argv[0])
    else:
        print (sys.argv[2])

if __name__ == '__main__' :
    main()
    IP_dictionary = {'MyIP':'0.0.0.0', 'switch maneger':'192.168.43.53'}
    s = Server('0.0.0.0',8000)
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
            Sendcmd = Client(ip, pt, cmd)
            Sendcmd.start()


