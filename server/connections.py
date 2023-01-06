import os
import socket
import threading
from users import User

MESSAGE_LENGTH = os.getenv('MESSAGE_LENGTH')
CLIENTS = []


def accept_connections(s):
    '''
    Accepts the connection
    '''
    while True:
        try:
            client, _ = s.accept()
        except OSError:
            print(OSError)

        # Save the client to a list
        CLIENTS.append(client)

        # Handle multiple clients
        handle_connections = threading.Thread(
            target=handle_multiple_connections, args=client)

        handle_connections.start()


def handle_multiple_connections(client):
    '''
    Listens for incoming messages from clients
    '''
    try:
        msg = client.recv(MESSAGE_LENGTH)
    except socket.error:
        print(socket.error)

    # Based on incoming message do actions

    # JOIN message accepts the JOIN followed by the username
    if msg.startswith('JOIN'):
        username = msg.split(' ')[1:]
        curr_user = User(client, username)
    else:
        pass
