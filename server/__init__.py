from log import logger, setup_log
import curses
from widgets import LogBox, header_widget
# import test
from time import sleep
from socketserver import SocketServer
from threading import Thread


class UI():
    def __init__(self):
        # Thread.__init__(self)
        # self.daemon = True
        self.screen = None
        self.socket_server = SocketServer("", 8888)

        self.maxx = None
        self.maxy = None

        self.run()

    def run(self):
        try:
            curses.wrapper(self.start_ui)
        except Exception as e:
            self.stop()
            print e

    def start_ui(self, stdscr):
        self.init_screen(stdscr)

        logbox = LogBox(14, self.maxx - 4, self.maxy - 14, 2)

        header_widget(1, self.maxx, 0, 0)

        self.socket_server.start()

        logbox.box.getch()
        self.socket_server.stop()
        self.stop()

    def init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

    def init_screen(self, stdscr):
        stdscr.nodelay(1)
        self.maxy, self.maxx = stdscr.getmaxyx()
        curses.setsyx(-1, -1)
        stdscr.refresh()
        self.init_colors()

    def stop(self):

        curses.curs_set(1)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
