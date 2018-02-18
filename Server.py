from Config import Config
import sys, socket

HOST = Config.SERVER_HOST
PORT = Config.SERVER_PORT

for each in sys.argv:
    if '--HOST=' in each:
        HOST = str(each[7:])
    elif '--PORT=' in each:
        PORT = int(each[7:])


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created on host: %s' % HOST)

try:
    sock.bind((HOST, PORT))
except socket.error as err:
    print('Bind failed. Error Code : ' .format(err))

sock.listen(10)
print("Socket Listening on port %d" % PORT)

while(True):
    try:
        conn, addr = sock.accept()
        conn.send(bytes("Message"+"\r\n",'UTF-8'))
        print("Message sent")
        data = conn.recv(1024)
        print(data.decode(encoding='UTF-8'))
    except socket.error as e:
        sock.close()
        print(e)
