from argparse import ArgumentParser
from socket import socket, AF_INET, SOCK_DGRAM

from atomic_p2p.local_monitor import LocalMonitor


class LoggerReceiver(LocalMonitor):
    def __init__(self, password, bind_address: str = "0.0.0.0", bind_port: int = 17032):
        super().__init__(
            service=None,
            password=password,
            bind_address=bind_address,
            bind_port=bind_port,
            loopDelay=0.1,
            logger=None,
        )

    def command_recv(self, enc_data, addr):
        if self.stopped.is_set() is False:
            data = self.decrypt(enc_data=enc_data).decode()
            if data is not None and data != "":
                print(data)


if __name__ == "__main__":

    def min_length(data):
        if len(data) % 16 != 0:
            return data + " " * (16 - len(data) % 16)
        else:
            return data

    parser = ArgumentParser()
    parser.add_argument("password", type=min_length)
    parser.add_argument("-ba", "--bind-address", type=str, default="0.0.0.0")
    parser.add_argument("-bp", "--bind-port", type=int, default=17032)
    parser.add_argument("-ta", "--target-address", type=str, default="localhost")
    arg = parser.parse_args()

    logRecver = LoggerReceiver(
        password=arg.password, bind_address=arg.bind_address, bind_port=arg.bind_port
    )
    logRecver.start()

    sock = socket(AF_INET, SOCK_DGRAM)

    while True:
        try:
            user_input = input("> ")
            if user_input.upper() == "C:CLOSE":
                sock.close()
            elif user_input.upper() == "C:STOP":
                logRecver.stop()
                break
            else:
                enc_data = logRecver.encrypt(raw_data=user_input)
                sock.sendto(enc_data, (arg.target_address, arg.bind_port - 1))
        except KeyboardInterrupt:
            sock.close()
            logRecver.stop()
            break
