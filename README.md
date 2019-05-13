# AtomicP2P  
[![PyPI version](https://badge.fury.io/py/AtomicP2P.svg)](https://badge.fury.io/py/AtomicP2P) [![Build Status](https://travis-ci.org/YuntechNet/AtomicP2P.svg?branch=fwos)](https://travis-ci.org/YuntechNet/AtomicP2P) [![codecov](https://codecov.io/gh/YuntechNet/AtomicP2P/branch/master/graph/badge.svg)](https://codecov.io/gh/YuntechNet/AtomicP2P) [![Maintainability](https://api.codeclimate.com/v1/badges/e02dfc9c29c0a9a053bc/maintainability)](https://codeclimate.com/github/YuntechNet/AtomicP2P/maintainability)  
A high-availability peer-to-peer framework which base on multi-process and threading with distribute and DNS syncing mechanism.  

## Feature
  1. High-Availability with whole network.
  2. Multiprocessing / threading with each peer.
  3. Healthy infrastructure to build top application.
  4. DNS syncing mechanism.
  5. Decentralized and Kubernets / docker friendly deployed.

## Installation
```sh
$ pip install AtomicP2P
```

## Contributing
Tag a commit with AtomicP2P's `__version__`.
```sh
# Add a simple tag.
$ grep '__version__ = ' atomic_p2p/__init__.py | cut -d "'" -f 2 | xargs git tag
# Add a tag with messages.
$ grep '__version__ = ' atomic_p2p/__init__.py | cut -d "'" -f 2 | xargs git tag -a
# Remove a tag.
$ grep '__version__ = ' atomic_p2p/__init__.py | cut -d "'" -f 2 | xargs git tag -d
```
