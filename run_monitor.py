import argparse
import socket
import base64
from threading import Thread
from Crypto.Cipher import AES

from atomic_p2p.manager import ThreadManager


class LoggerReceiver(ThreadManager):
    def __init__(self, password):
        super().__init__(loopDelay=0.1, logger=None)
        self.password = password
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("localhost", 17032))

    def registerHandler(self):
        pass

    def registerCommand(self):
        pass

    def new_cipher(self, key: str):
        return AES.new(key.encode(), AES.MODE_CBC, "0000000000000000".encode())

    def encrypt(self, raw_data):
        if len(raw_data) % 16 != 0:
            raw_data += " " * (16 - len(raw_data) % 16)
        return self.new_cipher(key=self.password).encrypt(raw_data.encode())

    def decrypt(self, enc_data):
        return self.new_cipher(key=self.password).decrypt(enc_data)

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            (data, addr) = self.sock.recvfrom(1024)
            thread = Thread(target=self.recv, args=(data, addr))
            thread.start()

    def recv(self, enc_data, addr):
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

    parser = argparse.ArgumentParser()
    parser.add_argument("password", type=min_length)
    arg = parser.parse_args()

    logRecver = LoggerReceiver(password=arg.password)
    logRecver.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
                sock.sendto(enc_data, ("localhost", 17031))
        except KeyboardInterrupt:
            sock.close()
            logRecver.stop()
            break
