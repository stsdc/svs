import socket
from log import logger

logger.info("-------------------------------------")
logger.info("|  *   Synergia Vision System    *  |")
logger.info("-------------------------------------")

if (socket.gethostname() == 'main_unit'):
    from server.ui2 import UI
    UI()
else:
    from client import Client
    Client()
