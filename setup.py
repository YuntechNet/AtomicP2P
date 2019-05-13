import os, sys
from setuptools import setup, find_packages
from atomic_p2p import __version__

_here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_here, 'README.md'), encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name = 'AtomicP2P',
    packages = find_packages(),
    version = __version__,
    license = 'GNU Lesser General Public License v2.1', 
    description = 'A P2P framework which base on multi-process and threading with DNS syncing mechanism.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Clooooode',
    author_email = 'jackey8616@gmail.com',
    url = 'https://github.com/YuntechNet/AtomicP2P',
    download_url = 'https://github.com/YuntechNet/AtomicP2P/releases/tag/{}'.format(__version__),
    keywords = ['peer-to-peer', 'P2P', 'p2p', 'distribute', 'HA', 'High-Availability'],
    install_requires = [
        'dnspython==1.16.0',
        'pycryptodome==3.8.1',
        'pyOpenSSL==19.0.0'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    python_requires=">=3.5"
)
