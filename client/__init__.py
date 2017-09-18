from log import logger
import socket
from time import sleep
from socketclient import Client

logger.debug("Initializing %s", socket.gethostname())

data = {
  'name': 'Patrick Jane',
  'age': 45,
  'children': ['Susie', 'Mike', 'Philip']
}
client = Client("10.0.0.1", 50000)
while True:
    try:
        client.send(data)
        sleep(1)
        response = client.recv()
        if not response:
            client.close()
            logger.warning ("No response. Exit...")
            break
        logger.debug (response)
    except socket.error, ex:
         logger.error(ex)
         client.close()
         break

logger.info("Done")
client.close()
