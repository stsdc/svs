import socket
from time import sleep
import json
from log import logger
from socketclient import SocketClient
from vision import MarkerDetector

logger.debug("Initializing %s", socket.gethostname())

# probably move this all data structure to vision?
# or just retrieve the data in one structure and jsonify here
# so detector thread wouldn't slowing down
def jsonify(marker):
    return json.dumps(make_dict(marker))

def make_dict(marker):
    # that's a huge mess. It should handle multiple markers.
    # marker is a tuple
    # isApple = True if fruit == 'Apple' else False
    values = ["", "", ""]
    if marker[0] is not None:
        values = [
            list(marker[0]),
            list(marker[1]),
            list(marker[2])
        ]
    keys = ['id', 'rotation', 'translation']
    return dict(zip(keys, values))

detector = MarkerDetector()

socket_client = SocketClient("10.0.0.1", 50000)
detector = MarkerDetector()
detector.start()
while True:
    try:
        socket_client.send(jsonify(detector.get_marker()))
        sleep(1)
        response = socket_client.recv()
        if not response:
            socket_client.close()
            logger.warning ("No response. Exit...")
            detector.stop()
            detector.join()
            break
        logger.debug (response)
    except (socket.error, KeyboardInterrupt) as e:
         logger.error(e)
         socket_client.close()
         detector.stop()
         detector.join()
         break



logger.info("Done")
socket_client.close()
