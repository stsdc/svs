from log import logger
import socket
form socketclient import Client

logger.debug("Initializing %s", socket.gethostname())

data = {
  'name': 'Patrick Jane',
  'age': 45,
  'children': ['Susie', 'Mike', 'Philip']
}
client = Client()
client.connect("10.0.0.1", 9000)
client.send(data)
response = client.recv()
client.close()
