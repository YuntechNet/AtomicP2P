import pytest
from os import getcwd, remove
from os.path import join
from OpenSSL.SSL import Context, TLSv1_METHOD, Error
from OpenSSL.crypto import load_privatekey, load_certificate, FILETYPE_PEM
from LibreCisco.utils.security import create_self_signed_cert

def test_create_self_signed_cert():
    cert_a, cert_k = create_self_signed_cert(join(getcwd(), 'data'), 'a.pem', 'a.key')
    cert_b, cert_b = create_self_signed_cert(join(getcwd(), 'data'), 'b.pem', 'b.key')
    key_a = load_privatekey(FILETYPE_PEM, open(join(getcwd(), 'data', 'a.key')).read())
    cert_a = load_certificate(FILETYPE_PEM, open(join(getcwd(), 'data', 'a.pem')).read())
    cert_b = load_certificate(FILETYPE_PEM, open(join(getcwd(), 'data', 'b.pem')).read())

    ctx = Context(TLSv1_METHOD)
    ctx.use_privatekey(key_a)
    ctx.use_certificate(cert_a)
    ctx.check_privatekey()
    ctx.use_certificate(cert_b)
    with pytest.raises(Error):
        ctx.check_privatekey()

    remove(join(getcwd(), 'data', 'a.pem'))
    remove(join(getcwd(), 'data', 'a.key'))
    remove(join(getcwd(), 'data', 'b.pem'))
    remove(join(getcwd(), 'data', 'b.key'))

