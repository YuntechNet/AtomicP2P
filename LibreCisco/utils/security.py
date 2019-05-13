from typing import Tuple
import hashlib
from os import listdir, getcwd
from os.path import join, isfile, isdir
from OpenSSL import crypto
from os.path import exists, join


def create_self_signed_cert(cert_dir: str, cert_file: str = 'myapp.crt',
                            key_file: str = 'myapp.key') -> Tuple[str, str]:
    """
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """

    if not exists(join(cert_dir, cert_file)) \
            or not exists(join(cert_dir, key_file)):
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)

        # create a self-signed cert
        cert = crypto.X509()
        subject = cert.get_subject()
        setattr(subject, 'C', 'US')
        setattr(subject, 'ST', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        setattr(subject, 'L', 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        setattr(subject, 'O', 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
        # XD
        setattr(subject, 'OU', 'bunny corp')
        setattr(subject, 'CN', 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha256')

        with open(join(cert_dir, cert_file), "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        with open(join(cert_dir, key_file), "wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    return cert_file, key_file


def self_hash(path: str) -> str:
    hash_str = ''
    for each in listdir(path):
        if isdir(join(path, each)):
            hash_str += self_hash(join(path, each))
        elif isfile(join(path, each)):
            with open(join(path, each), 'rb') as f:
                hash_str += hashlib.sha256(f.read()).hexdigest()
    return hashlib.sha256(bytes(hash_str, encoding='utf-8')).hexdigest()
