from socketserver import SocketServer
from threading import Thread, Event
from steerage import Steerage
from log import logger
from events import Events
from control import Manipulator, MobilePlatform
from uart import Uart

class Core(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

        self.events = Events()

        # Init uart and control MP & Manipulator
        self.uart = Uart()
        if self.uart.serial:
            self.manipulator = Manipulator(self.uart)
            self.mobile_platform = MobilePlatform(self.uart)
            Steerage(self.manipulator, self.mobile_platform)

        self.unit0 = {}
        self.unit1 = {}
        self.markerA = 0
        self.markerB = 0

        self.snaps = {
            "unit0": {"A": [], "B": []},
            "unit1": {"A": [], "B": []}
        }

        self.distance = None
        self.sockserver = SocketServer("", 50000)

        self.sockserver.events.on_connected += self.referencing_clients_to_core
        # self.manipulator.events.on_data += self.update_manipulator_ui



    def run(self):
        self.sockserver.start()

    def distance(self, data):
        pass

    # pos is unused, but needed
    def make_snap(self, pos):
        logger.info("SNAP")

    def area(self):
        pass


    def __stop(self):
        self.sockserver.stop()

    # this looks really lame
    def referencing_clients_to_core(self, is_connected):
        if is_connected:
            self.unit0 = self.sockserver.threads[0]
            self.unit0.events.on_new_data += self.update_unit0
            if len(self.sockserver.threads) > 1:
                self.unit1 = self.sockserver.threads[1]
                self.unit1.events.on_new_data += self.update_unit1
        else:
            self.unit0 = {}
            self.unit1 = {}

    def update_unit0(self, data):
        # self.distance()
        self.events.update_unit0_ui(data["markers"])

