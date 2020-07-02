#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example program on how a server can be easily created in Python.

This program allows the server to send messages out to clients. With some work,
the code could be modified to allow clients to communicate with each other."""

import datetime
import socket
import sys
import threading

# Public Names
__all__ = (
    'LOCAL_ADDRESS',
    'SERVER_PORT',
    'main',
    'handle_connections',
    'run_communication_loop',
    'shutdown_server',
    'broadcast_message',
    'shutdown_client'
)

# Symbolic Constants
LOCAL_ADDRESS = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 8090

# Module Documentation
__version__ = 1, 0, 0
__date__ = datetime.date(2020, 7, 2)
__author__ = 'Stephen Paul Chappell'
__credits__ = 'Summer Computer Science Camp'


def main():
    """Create a server that allows messages to be sent to connected clients."""
    clients = set()
    threading.Thread(target=handle_connections, args=(clients,)).start()
    run_communication_loop(clients)


def handle_connections(clients):
    """Accept incoming connections and place them in the clients set."""
    server = socket.create_server(('', 8090))
    while True:
        client, address = server.accept()
        if address == LOCAL_ADDRESS:
            server.close()
        client.setblocking(False)
        clients.add(client)


def run_communication_loop(clients):
    """Allow the server to send messages to anyone who is connected."""
    while True:
        try:
            message = input('Say: ')
        except (EOFError, KeyboardInterrupt):
            shutdown_server(clients)
        else:
            broadcast_message(clients, message.encode('ascii'))


def shutdown_server(clients):
    """Create a connection to the server so that it will stop running."""
    client = socket.create_connection((LOCAL_ADDRESS, SERVER_PORT))
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    for client in clients.copy():
        shutdown_client(clients, client)
    sys.exit()


def broadcast_message(clients, message):
    """Try to send a message to all connected clients while handling errors."""
    for client in clients.copy():
        try:
            client.sendall(message)
        except socket.timeout:
            shutdown_client(clients, client)


def shutdown_client(clients, client):
    """Properly disconnect a client from the server."""
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    clients.remove(client)


if __name__ == '__main__':
    main()
