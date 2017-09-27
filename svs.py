import socket
import log
from cron import Cron

Cron().check()

# if (socket.gethostname() == 'main_unit'):
#     from server import Server
#     Server()
# else:
#     from client import Client
#     Client()
