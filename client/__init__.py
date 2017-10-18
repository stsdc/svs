import socket
from time import sleep
import os
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
        # Cron().check()
        # while not Network().connect():
        #     sleep(10)
        #     continue

        self.marker_detector = MarkerDetector()

        self.socket_client = SocketClient("10.0.0.1", 50000)

    def pack_markers(self, (ids, rotations, translations)):
        markers = []
        marker = {
            "id": -1,
            "rot": [],
            "tran": []
        }
        if ids is not None:
            # ids = list(ids)
            for index, id in enumerate(ids):
                marker = {
                "id": id[0],
                "rot": list(rotations[index][0]),
                "tran": list(translations[index][0])
                }
                markers.append(marker)
        return markers

    def pack_telemetry(self):
        temp = os.popen("cat /sys/devices/virtual/thermal/thermal_zone1/temp").readline()
        temp = temp.replace("\n", "")
        telemetry = {
            "temp": temp
        }
        return telemetry

    def pack_all_data(self, marker):
        return {
            "telemetry": self.pack_telemetry(),
            "markers": self.pack_markers(marker)
        }

    def close(self):
        self.socket_client.close()
        self.marker_detector.stop()
        self.marker_detector.join()

    def run(self):
        self.socket_client.connect()
        self.marker_detector.start()
        while True:
            try:
                # self.socket_client.send(self.make_dict(self.marker_detector.get_marker()))
                print self.pack_all_data(self.marker_detector.get_marker())

                sleep(0.5)
                # response = self.socket_client.recv()
                # if not response:
                #     logger.warning("No response. Exit...")
                #     self.close()
                #     break
                # logger.debug(response)
            except socket.error as e:
                logger.error("SocketClient: %s", e)
                self.close()
                break
            except KeyboardInterrupt:
                logger.warning("SocketClient: Closing...")
                self.close()
                break
