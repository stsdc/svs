from socketserver import SocketServer
from log import logger
from hotspot import HotSpot
from time import sleep

logger.debug("Initializing Main Unit")

# server = Server("", 8888)
# try:
#     while True:
#         server.accept()
#         data = server.recv()
#         # shortcut: data = server.accept().recv()
#         server.send({'status': 'ok'})
# except (TypeError, ValueError), e:
#     logger.exception("Unexpected exception: ", e)
# finally:
#     logger.info("Shutting down")
#     server.close()

# server = Server("", 50000)
# server.run()


class Server(object):
    def __init__(self):
        self.socket_server = SocketServer("", 8888)
        self.waiter()

    def check_connectivity(self):
        hotspot = HotSpot()
        if bool(hotspot.clients):
            for mac in hotspot.clients:
                logger.info("HotSpot: Connected client: %s, %s, %s", hotspot.clients[mac][4], hotspot.clients[mac][3], hotspot.clients[mac][5])
            return True
        else:
            logger.warning("HotSpot: No clients")
        return False

    def waiter(self):
        is_client_connected = False
        while is_client_connected is not True:
            sleep(3)
            is_client_connected = self.check_connectivity()
        try:
            self.socket_server.run()
        except BaseException as e:
            logger.error("Error when starting server: %s", e)
            logger.warning("Checking connection and restarting server")
            self.waiter()
