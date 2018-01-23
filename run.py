import getpass
from OPxssh import OPxssh

def ssh_open(host="",userName="",parameter="",password=""):
    command = 'ssh '+userName+'@'+host+' '+parameter
    print(command)
    conection=pexpect.spawn(command)
    conection.expect('assword: ') #possbile P or p
    conection.sendline(password)
    conection.expect(r"[\#]")
    conection.sendline('show arp')
    conection.expect(r"[\#]")
    print(conection)
    while True:
        command = input('command: ')
        conection.sendline(command)
        conection.expect(r"[\#]",timeout=1)
        print(conection.before)

def ssh_pxssh(host="",userName="",password="",options={},parameter=""):
    print(options)
    s = OPxssh(options=options)
    s.login(server=host,username=userName,password=password,parameter=parameter)
    print(s.before)
    while True:
        command = input("command: ")
        s.sendline(command)
        s.prompt()
        print(s)

host = input('host: ')
userName = input('userName: ')
password = getpass.getpass()


parameter = "-oKexAlgorithms=+diffie-hellman-group1-sha1"
options={"-oKexAlgorithms":"+diffie-hellman-group1-sha1"}

#ssh_open(host=host,userName=userName,password=password,parameter=parameter)
ssh_pxssh(host=host,userName=userName,password=password,options=options,parameter=parameter)
