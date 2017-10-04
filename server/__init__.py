from widgets import LogBox, HeaderBox, Screen
from time import sleep
from socketserver import SocketServer

class UI():
    def __init__(self):

        self.screen = Screen()
        self.socket_server = SocketServer("", 8888)

        self.maxx = self.screen.maxx
        self.maxy = self.screen.maxy

        self.start_ui()

    def start_ui(self):
        # self.init_screen(stdscr)

        logbox = LogBox(14, self.maxx - 4, self.maxy - 14, 2)
        HeaderBox(1, self.maxx, 0, 0)

        self.socket_server.start()

        logbox.box.getch()
        self.socket_server.stop()
        self.screen.stop()

