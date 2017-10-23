from socketserver import SocketServer
from threading import Thread, Event
from steerage import Steerage
from log import logger


class Core(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

        Steerage()

        self.snaps = {
            "unit0": {"A": [], "B": []},
            "unit1": {"A": [], "B": []}
        }

        self.distance = None
        self.sockserver = SocketServer("", 50000)




    def run(self):
        self.sockserver.start()

    def distance(self):
        pass

    # pos is unused, but needed
    def make_snap(self, pos):
        logger.info("SNAP")

    def area(self):
        pass


    def __stop(self):
        self.sockserver.stop()
