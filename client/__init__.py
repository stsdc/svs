import socket
from time import sleep
import json
from log import logger
from socketclient import Client
from vision import MarkerDetector

logger.debug("Initializing %s", socket.gethostname())

# probably move this all data structure to vision?
# or just retrieve the data in one structure and jsonify here
# so detector thread wouldn't slowing down
def jsonify(data):
    if data is not None:
        print "translation" + str(detector.translation[0][0])
        return json.dumps({
            "is_marker": True,
            "translation": list(data[0][0])
        })
    else:
        return json.dumps({
            "is_marker": False
        })


detector = MarkerDetector()

client = Client("10.0.0.1", 50000)
detector = MarkerDetector()
detector.start()
while True:
    try:
        client.send(jsonify(detector.translation))
        sleep(1)
        response = client.recv()
        if not response:
            client.close()
            logger.warning ("No response. Exit...")
            detector.stop()
            detector.join()
            break
        logger.debug (response)
    except (socket.error, KeyboardInterrupt) as e:
         logger.error(e)
         client.close()
         detector.stop()
         detector.join()
         break



logger.info("Done")
client.close()
