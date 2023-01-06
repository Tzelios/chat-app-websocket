import os
import socket
import threading

from dotenv import load_dotenv

from users import User

load_dotenv()
MESSAGE_LENGTH = int(os.getenv('MESSAGE_LENGTH'))
CLIENTS = []


def accepta_connections(s):
    '''
    Accepts the connection
    '''
    while True:
        try:
            client, _ = s.accept()
        except OSError:
            print(OSError.strerror)

        # Save the client to a list
        CLIENTS.append(client)

        # Handle multiple clients
        handle_connections = threading.Thread(
            target=handle_multiple_connections, args=(client, ))

        handle_connections.start()


def handle_multiple_connections(client):
    '''
    Listens for incoming messages from clients
    '''
    curr_user = None
    while True:
        try:
            msg = client.recv(MESSAGE_LENGTH).decode('utf-8')
        except socket.error:
            print(socket.error.strerror)

        # Based on incoming message do actions

        # JOIN message accepts the JOIN followed by the username
        if msg.startswith('JOIN'):
            if curr_user is None:
                username = ' '.join(msg.split(' ')[1:])
                curr_user = User(client, username)
                continue
        else:
            pass
