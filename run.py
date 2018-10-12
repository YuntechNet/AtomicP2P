from peer import Peer
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
        peer.sendMessage((target.split(':')[0], target.split(':')[1]), 'join')
    else:
        print('you are first peer \n')
   
    helptips="Send: send message .\n" + "list: show the connectlist .\n"
    print(helptips)
    
    while True:
        cmd = input()
        if cmd=='help':
            print(helptips)
        elif cmd == 'Send':
            try:
                ip = str(input ('host:'))
                port = input ('port:')
                mes = {'msg': input('message:')}
                print('send to',ip,port)
                peer.sendMessage((ip, port),'message', **mes)
       
            except ValueError:
                print ("wrong input\n")  

        elif cmd == 'broadcast':
            data = {
                'role': input('input aim of broadcast:'),
                'msg': input('message:')
            }
            for member in peer.connectlist:
                peer.sendMessage((member.host[0], member.host[1]), 'broadcast', **data)
                
        elif cmd=='list':
            for each in peer.connectlist:
                print(each)
        elif cmd=='exit':
            peer.stop()
            break

        elif cmd=='test':
            mes=input()
            if mes == 'role':
                print(peer.role)
            if mes == 'port':
                print(peer.listenPort)
            if mes == 'name':
                print(peer.name)
        else:
            print('command error , input "help" to check the function.')


if __name__ == '__main__' :
    main()
