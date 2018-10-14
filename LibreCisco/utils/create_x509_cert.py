#!/usr/bin/env python

from OpenSSL import crypto
from os.path import exists, join


def create_self_signed_cert(cert_dir, cert_file='myapp.crt', key_file='myapp.key'):
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
        cert.get_subject().C = "US"
        cert.get_subject().ST = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        cert.get_subject().L = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        cert.get_subject().O = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"
        # XD
        cert.get_subject().OU = "bunny corp"
        cert.get_subject().CN = "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
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

