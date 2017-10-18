from socketserver import SocketServer
from threading import Thread, Event


class Core(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

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

    def make_snap(self):
        pass

    def area(self):
        pass

    def __stop(self):
        self.sockserver.stop()
