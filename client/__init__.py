from log import logger
import socket

logger.debug("Initializing %s", socket.gethostname())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("10.0.0.1", 9000))
data = "some data"
sock.sendall(data)
result = sock.recv(1024)
print result
sock.close()
