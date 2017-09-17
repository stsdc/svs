from socketserver import Server
from log import logger

logger.debug("Initializing Main Unit")

try:
    server = Server("", 9000)
    while True:
        server.accept()
        data = server.recv()
        # shortcut: data = server.accept().recv()
        server.send({'status': 'ok'})
except (TypeError, ValueError), e:
    logger.exception("Unexpected exception: ", e)
finally:
    logger.info("Shutting down")
    server.close()
