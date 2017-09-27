import socket
from log import logger
from cron import Cron

logger.info("-------------------------------------")
logger.info("|  *   Synergia Vision System    *  |")
logger.info("-------------------------------------")

Cron().check()

if (socket.gethostname() == 'main_unit'):
    from server import Server
    Server()
else:
    from client import Client
    Client()
