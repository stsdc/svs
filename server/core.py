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
        # self.daemon = True

        self.events = Events()

        self.socket_server = SocketServer("", 50000)
        self.uart = Uart()
        self.manipulator = None
        self.mobile_platform = None

        self.unit0 = {}
        self.unit1 = {}
        self.TOP_MARKER = 9
        self.SIDE_MARKER = 16

        self.snaps = {
            "unit0": {"TOP_MARKER": [], "SIDE_MARKER": []},
            "unit1": {"TOP_MARKER": [], "SIDE_MARKER": []}
        }

        self.distance = None

    def run(self):
        self.socket_server.start()
        self.uart.start()

        self.connect_events()

    def connect_events(self):
        self.uart.events.on_connected += self.start_control
        self.socket_server.events.on_connected += self.referencing_clients_to_core

    def start_control(self):
        # Only when serial is connected
        if self.uart.serial:
            self.manipulator = Manipulator(self.uart)
            self.mobile_platform = MobilePlatform(self.uart)
            Steerage(self.manipulator, self.mobile_platform)
            self.manipulator.events.on_data += self.update_manipulator_ui

    def distance(self, data):
        pass

    # pos is unused, but needed
    def make_snap(self, pos):
        logger.info("SNAP")

    def area(self):
        pass

    def __stop(self):
        self.manipulator.stop()
        self.uart.stop()
        self.socket_server.stop()
        self.join()

    # this looks really lame
    def referencing_clients_to_core(self, is_connected):
        if is_connected:
            self.unit0 = self.socket_server.threads[0]
            self.unit0.events.on_new_data += self.update_unit0
            if len(self.socket_server.threads) > 1:
                self.unit1 = self.socket_server.threads[1]
                self.unit1.events.on_new_data += self.update_unit1
        else:
            self.unit0 = {}
            self.unit1 = {}

    def update_unit0(self, data):
        # self.distance()
        self.events.update_unit0_ui(data["markers"])

    def update_unit1(self, data):
        # self.distance()
        self.events.update_unit1_ui(data["markers"])

    def update_manipulator_ui(self, data):
        self.events.update_manipulator_ui(data)
