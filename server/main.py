import os
import sys
import json
import socket
import threading

from dotenv import load_dotenv

from connections import accepta_connections
from users import User

load_dotenv()
IP = os.getenv('SERVER_IP')
PORT = int(os.getenv('SERVER_PORT'))


def main():

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP, PORT))
        server.listen()
    except socket.error:
        print(socket.error.strerror)
        server.close()
        sys.exit()

    connentions = threading.Thread(target=accepta_connections, args=(server, ))
    connentions.start()


if __name__ == '__main__':
    main()
