import os
import sys
import json
import socket
import threading

from dotenv import load_dotenv

from connections import accept_connections
from users import User

load_dotenv()
IP = os.getenv('SERVER_IP')
PORT = os.getenv('SERVER_PORT')


def main():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP, PORT))
        server.listen()
    except socket.error:
        print(socket.error)
        sys.exit()

    threading.Thread(target=accept_connections, args=server)


if __name__ == 'main':
    main()
