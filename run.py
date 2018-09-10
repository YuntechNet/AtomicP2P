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
        peer = Peer(addr.split(':')[0], int(addr.split(':')[1]), name )        
    else:
        peer = Peer() 
    peer.start()

    if linkaddr:
        peer.sendMessage( linkaddr.split(':')[0], int(linkaddr.split(':')[1]), "join", [name, peer.listenPort ] )
    else:
        print('you are first peer')

    helptips="Send: send message .\n" + "list: show the connectlist .\n"
    print(helptips)
    
    while True:
        cmd = input()
        if cmd=='help':
            print(helptips)
        elif cmd == 'Send':
            ip = str(input ('host:'))
            port = int(input ('port:'))
            mes = input('message:')
            print('send to',ip,port)
            peer.sendMessage( ip, port,"message", mes)
        elif cmd=='list':
            print(peer.connectlist)
        elif cmd=='exit':
            pass
        else:
            print('command error , input "help" to check the function.')

if __name__ == '__main__' :
    main(sys.argv)