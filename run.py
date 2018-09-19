from peer.peer import Peer
import sys
import click


@click.command()
@click.option('--role' , default='core' , help='role of peer.')
@click.option('--addr' , default='0.0.0.0:8000' , help='self addresss.')
@click.option('--target' , default='0.0.0.0:8000' , help='target addresss.')
@click.option('--name' , default='core' , help='peer name.')
def main(role, addr, target, name): 
    """LibreCisco Test Version"""
   
    peer = Peer(addr.split(':')[0], int(addr.split(':')[1]), name ,role)        
    
    peer.start()  

    if ( target != '0.0.0.0:8000' ):
        peer.sendMessage( target.split(':')[0], int(target.split(':')[1]), "join", [name, peer.listenPort ] )
    else:
        print('you are first peer')
   
    helptips="Send: send message .\n" + "list: show the connectlist .\n"
    print(helptips)
    
    while True:
        cmd = input()
        if cmd=='help':
            print(helptips)
        elif cmd == 'Send':
            try:
                ip = str(input ('host:'))
                port = int(input ('port:'))
                mes = input('message:')
                print('send to',ip,port)
                peer.sendMessage( ip, port,"message", mes)
       
            except ValueError:
                print ("wrong input\n")  

        elif cmd == 'broadcast':
            broadType = input('input aim of broadcast:')
            mes = input('message:')
            for member in peer.connectlist:
                peer.sendMessage(member[2], member[1], 'broadcast', [peer.name, broadType, mes])
                
        elif cmd=='list':
            print(peer.connectlist)
        elif cmd=='exit':
            peer.stop()
            break
        else:
            print('command error , input "help" to check the function.')
    print('disconnect successful')

if __name__ == '__main__' :
    main()