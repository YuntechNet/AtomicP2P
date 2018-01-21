from pexpect import pxssh
import pexpect
import getpass

def ssh_open(host="",userName="",parameter="",password=""):
    command = 'ssh '+userName+'@'+host+' '+parameter
    conection=pexpect.spawn(command)
    conection.expect('password: ')
    conection.sendline(password)
    conection.expect(userName+'@')
    conection.sendline('ls')
    conection.expect(r"[\$]")
    print(conection)
    while True:
        command = input('command: ')
        conection.sendline(command)
        conection.expect(r"[#$]",timeout=1)
        print(conection)

def ssh_pxssh(host="",userName="",password="",options={}):
    s = pxssh.pxssh()
    s.login(host,userName,password)
    print(s.before)
    while True:
        command = input("command: ")
        s.sendline(command)
        s.prompt("a")
        print(s)

host = input('host: ')
userName = input('userName: ')
password = getpass.getpass()

ssh_open(host=host,userName=userName,password=password)
#ssh_pxssh(host=host,userName=userName,password=password)
