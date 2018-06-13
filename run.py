from peer.peer import Peer
import sys

def main(argv): 
    '''
    輸入方式: python --addr=0.0.0.0:8000 --link=192.168.43.53:8000 --name=XX
    '''
    addr = None
    linkaddr = None
    name = None
    for arguments in argv:
        if '--addr=' in arguments:
            if ':' in arguments:
                addr = arguments[7:]
            else:
                addr = arguments[7:] + ':8000'

        if '--link=' in arguments:
            if ':' in arguments:
                linkaddr = arguments[7:]            
       
        if '--name' in arguments:
            name= arguments[7:]

    if addr:
        peer = Peer(addr.split(':')[0], int(addr.split(':')[1]) )        
    else:
        peer = Peer() 
        peer.start()

    if linkaddr:
        peer.sendMessage( linkaddr.split(':')[0], int(linkaddr.split(':')[1]), "join", [name, peer.listenPort ] )
    else:
        print('you are first peer')


    while True:
        cmd = input('imput what do you want to do:')
        if cmd=='help':
            print('S: send your message to aim.')
        elif cmd == 'S':
            ip = str(input ('host:'))
            pt = int(input ('port:'))
            cmd = input('command:')
            print('send to',ip,pt)
            peer.sendMessage( ip, pt,"command", cmd)
        elif cmd=='list':
            print(peer.connectlist)
        elif cmd=='exit':
            peer.sendMessage(None, 0, "exit", peer.connectlist)

if __name__ == '__main__' :
    main(sys.argv)