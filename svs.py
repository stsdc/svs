import socket
import log

if (socket.gethostname() == 'main_unit'):
    from server import Server
    Server()
else:
    from client import Client
    Client()
