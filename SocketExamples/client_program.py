#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example program on how a server can be easily created in Python.

This program allows the server to send messages out to clients. With some work,
the code could be modified to allow clients to communicate with each other."""

import datetime
import socket

# Public Names
__all__ = (
    'SERVER_PORT',
    'main',
)

# Symbolic Constants
SERVER_PORT = 8090

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2020, 7, 2)
__author__ = 'Stephen Paul Chappell'
__credits__ = 'Summer Computer Science Camp'


def main():
    """Create a client socket that will receive server messages."""
    server_addr = input('What is the name of the server? ')
    client_socket = socket.create_connection((server_addr, SERVER_PORT))
    try:
        while True:
            message = client_socket.recv(1 << 12)
            if not message:
                break
            print(message.decode('ascii'))
    except (KeyboardInterrupt, socket.error):
        pass
    finally:
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()


if __name__ == '__main__':
    main()
