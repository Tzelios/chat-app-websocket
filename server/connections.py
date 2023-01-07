from ctypes import sizeof
import json
import sys
import os
import socket
import threading

from dotenv import load_dotenv

from users import User

load_dotenv()
MESSAGE_LENGTH = int(os.getenv('MESSAGE_LENGTH'))
CLIENTS = []
USERNAMES = []


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
    collect_message = ''
    curr_user = False

    while True:
        try:
            msg = client.recv(MESSAGE_LENGTH).decode('utf-8')
        except socket.error:
            print(socket.error.strerror)

        # Based on incoming message do actions
        collect_message += msg
        if collect_message.startswith('START ') and collect_message.endswith(' END'):
            collect_message = collect_message.replace(
                'START ', '').replace(' END', '')

            data = json.loads(collect_message.strip())
            method = data['method']
            username = data['username']
            if not curr_user:
                if method == 'JOIN':
                    curr_user = True
                    USERNAMES.append(username)
                    msg = {
                        'users': USERNAMES,
                        'event': 'new_user',
                        'data': {
                            'username': username,
                            'msg': 'connected'
                        }
                    }
                    m = f"START {json.dumps(msg)} END"
                    message = m.encode('utf-8')
                    for cli in CLIENTS:
                        cli.send(message)

            elif method == 'LEAVE':
                for user in USERNAMES:
                    if user == username:
                        USERNAMES.remove(user)
                for user in CLIENTS:
                    if user.username == username:
                        CLIENTS.remove(user)

                msg = {
                    'username': username,
                    'event': 'user_left',
                    'data': {
                        'msg': 'disconect'
                    }
                }
                m = f"START {json.dumps(msg)} END"
                message = m.encode('utf-8')
                client.send(message)
                client.close()

            collect_message = ''
