from socketserver import SocketServer
from threading import Thread, Event
from radiocontrol import RadioControl
from log import logger
from steerage import Steerage


class Core(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

        self.snaps = {
            "unit0": {"A": [], "B": []},
            "unit1": {"A": [], "B": []}
        }

        self.distance = None

        self.motor_power = 20
        self.rc = RadioControl()
        self.steerage = Steerage()
        self.sockserver = SocketServer("", 50000)

        # self.control.bd.when_double_pressed = self.make_snap
        self.steerage.events.forward += self.move
        self.steerage.events.stop += self.move

    def run(self):
        self.sockserver.start()

    def distance(self):
        pass

    # pos is unused, but needed
    def make_snap(self, pos):
        logger.info("SNAP")

    def area(self):
        pass

    def move(self, motor_l, motor_r):
        self.rc.send(motor_l * self.motor_power, motor_r * self.motor_power)

    def __stop(self):
        self.sockserver.stop()
