from log import logger
import socket
from socketclient import Client

logger.debug("Initializing %s", socket.gethostname())

data = {
  'name': 'Patrick Jane',
  'age': 45,
  'children': ['Susie', 'Mike', 'Philip']
}
try:
    client = Client("10.0.0.1", 50000)
    client.send(data)
    response = client.recv()
    print response
    client.close()
except socket.error, ex:
     logger.error(ex)
