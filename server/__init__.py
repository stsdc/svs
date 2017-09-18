from socketserver import Server
from log import logger

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

server = Server("", 50000)
server.run()
