from widgets import LogBox, HeaderBox, Screen, InfoBox
from network import Network
from log import logger
import os
from time import sleep
from socketserver import SocketServer


class UI():
    def __init__(self):
        self.screen = Screen()
        self.socket_server = SocketServer("", 50000)
        self.socket_server.events.on_change += self.update_server_status
        self.net = Network()

        self.maxx = self.screen.maxx
        self.maxy = self.screen.maxy

        # UI elements
        self.headerbox = HeaderBox(1, self.maxx, 0, 0)
        self.serverbox = InfoBox(10, 25, 2, 2)
        self.logbox = LogBox(14, self.maxx - 4, self.maxy - 14, 2)

        self.start_ui()

    def start_ui(self):
        # self.init_screen(stdscr)


        self.build_serverbox()
        self.socket_server.start()
        # sleep(5)
        # logger.debug("%s", len(self.socket_server.threads))
        # client.on("new_data", self.show_data)

        self.logbox.box.getch()
        self.socket_server.stop()
        self.screen.stop()

    def build_serverbox(self):
        self.serverbox.add(0, 0, "PID:")
        self.serverbox.add(0, 7, "%16s" % os.getpid())
        self.serverbox.add(1, 0, "ETH:")
        self.serverbox.add(1, 7, "%16s" % self.net.eth_ip())
        self.serverbox.add(2, 0, "WLAN:")
        self.serverbox.add(2, 7, "%16s" % self.net.wlan_ip())
        self.serverbox.add(3, 0, "STATUS:")
        self.serverbox.add(3, 7, "%16s" % "DISCONNECTED")

    def show_data(self, data):
        logger.debug("%s", data)

    def update_server_status(self, status):
        if status:
            self.serverbox.add(3, 7, "%16s" % "CONNECTED")
