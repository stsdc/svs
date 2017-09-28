import socket
from log import logger

logger.info("-------------------------------------")
logger.info("|  *   Synergia Vision System    *  |")
logger.info("-------------------------------------")

if (socket.gethostname() == 'main_unit'):
    from server import Server
    Server()
else:
    from client import Client
    Client()
