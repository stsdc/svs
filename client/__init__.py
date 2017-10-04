import json
import socket
from time import sleep

from cron import Cron
from log import logger, run_coloredlogs
from markerdetector import MarkerDetector
from network import Network
from socketclient import SocketClient

run_coloredlogs()
logger.info("-------------------------------------")
logger.info("|  *   Synergia Vision System    *  |")
logger.info("-------------------------------------")


class Client(object):

    def __init__(self):
        logger.debug("Initializing %s", socket.gethostname())
        Cron().check()
        while not Network().connect():
            sleep(10)
            continue
        self.marker_detector = MarkerDetector()
        self.socket_client = SocketClient("10.0.0.1", 50000)

    # probably move this all data structure to vision?
    # or just retrieve the data in one structure and jsonify here
    # so detector thread wouldn't slowing down
    def jsonify(self, marker):
        return json.dumps(self.make_dict(marker))

    def make_dict(self, marker):
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

    def close(self):
        self.socket_client.close()
        self.marker_detector.stop()
        self.marker_detector.join()

    def run(self):
        self.marker_detector.start()
        # check if thread is alive
        while True:
            try:
                self.socket_client.send(self.jsonify(self.marker_detector.get_marker()))
                sleep(1)
                response = self.socket_client.recv()
                if not response:
                    logger.warning("No response. Exit...")
                    self.close()
                    break
                logger.debug(response)
            except (socket.error, KeyboardInterrupt) as e:
                logger.error(e)
                self.close()
                break
