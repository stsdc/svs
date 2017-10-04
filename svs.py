import socket

if socket.gethostname() == 'main_unit':
    from server import UI
    UI()
else:
    from client import Client
    Client()
