from widgets import LogBox, HeaderBox, Screen, InfoBox
from network import Network
import os
from time import sleep
from socketserver import SocketServer


class UI():
    def __init__(self):
        self.screen = Screen()
        self.socket_server = SocketServer("", 50000)
        self.net = Network()

        self.maxx = self.screen.maxx
        self.maxy = self.screen.maxy

        self.start_ui()

    def start_ui(self):
        # self.init_screen(stdscr)

        logbox = LogBox(14, self.maxx - 4, self.maxy - 14, 2)
        HeaderBox(1, self.maxx, 0, 0)
        self.serverbox()
        self.socket_server.start()

        logbox.box.getch()
        self.socket_server.stop()
        self.screen.stop()

    def serverbox(self):
        infobox = InfoBox(10, 25, 2, 2)
        infobox.add(0, 0, "PID:")
        infobox.add(0, 7, "%16s" % os.getpid())
        infobox.add(1, 0, "ETH:")
        infobox.add(1, 7, "%16s" % self.net.eth_ip())
        infobox.add(2, 0, "WLAN:")
        infobox.add(2, 7, "%16s" % self.net.wlan_ip())
