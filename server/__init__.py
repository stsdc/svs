from widgets import LogBox, HeaderBox, Screen, ServerBox, ClientBox
from network import Network
from log import logger
from core import Core
import os
import keyboard
from time import sleep


class UI():
    def __init__(self):
        self.screen = Screen()

        self.client0 = None

        self.maxx = self.screen.maxx
        self.maxy = self.screen.maxy

        # UI elements
        self.headerbox = HeaderBox(1, self.maxx, 0, 0)
        self.serverbox = ServerBox(10, 25, 2, 2)
        self.clientbox0 = ClientBox(20, 25, 2, 30)
        self.logbox = LogBox(14, self.maxx - 4, self.maxy - 14, 2)

        self.core = Core()
        self.core.sockserver.events.on_change += self.update_server_status

        self.start_ui()

    def start_ui(self):
        # self.init_screen(stdscr)
        self.core.start()

        # sleep(5)
        # logger.debug("%s", len(self.socket_server.threads))
        # client.on("new_data", self.show_data)

        # keyboard.wait('q')  # if key 'q' is pressed
        # self.logbox.box.getch()
        # self.socket_server.stop()
        # self.screen.stop()

        # key = ""
        # while key != ord('q'):  # press <Q> to exit the program
        self.logbox.box.getch()  # get the key

        self.stop()

    def show_data(self, data):
        logger.debug("%s", data)

    def update_server_status(self, status):
        self.serverbox.update_status(status)

        client0 = self.core.sockserver.threads[0]
        client0.events.on_new_data += self.show_data


    def update_client0(self, data):
        self.clientbox0.update_data(data)

    def stop(self):
        self.serverbox.close()
        self.core.join()
        self.screen.stop()

