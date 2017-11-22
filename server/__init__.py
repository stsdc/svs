from widgets import LogBox, HeaderBox, Screen, ServerBox, ClientBox, ManipulatorBox
from network import Network
from log import logger
from core import Core
from peripherals import Keyboard
import os
from time import sleep


class UI():
    def __init__(self):
        self.keyboard = Keyboard()

        self.screen = Screen()

        self.keyboard.events.refresh += self.refresh

        self.client0 = None

        self.maxx = self.screen.maxx
        self.maxy = self.screen.maxy

        # UI elements
        self.headerbox = HeaderBox(1, self.maxx, 0, 0)
        self.serverbox = ServerBox(13, 25, 2, 2)
        self.clientbox0 = ClientBox(13, 50, 2, 30, "Client1")
        self.clientbox1 = ClientBox(13, 50, 2, 80, "Client2")
        self.manipulatorbox = ManipulatorBox(13, 78, 16, 2)
        self.logbox = LogBox(14, self.maxx - 4, self.maxy - 14, 2)

        self.core = Core()

    def start_ui(self):
        # self.init_screen(stdscr)
        self.core.start()

        self.connect_events()

        self.logbox.box.getch()  # get the key

        self.stop()

    def connect_events(self):
        self.core.sockserver.events.on_connected += self.update_server_status
        self.core.events.update_unit0_ui += self.update_client0
        self.core.events.update_manipulator_ui += self.update_manipulator

    def show_data(self, data):
        logger.debug("%s", data)

    def update_server_status(self, status):
        self.serverbox.update_status(status)


    def update_client0(self, data):
        self.show_data(data)
        self.clientbox0.update_data(data)

    def update_manipulator(self, data):
        # self.show_data(data)
        self.manipulatorbox.update(data)

    def stop(self):
        self.serverbox.close()
        self.core.join()
        self.screen.stop()

    def refresh(self):
        self.headerbox.refresh()
        self.logbox.refresh()
        self.manipulatorbox.refresh()
        self.clientbox0.refresh()
        self.serverbox.refresh()

