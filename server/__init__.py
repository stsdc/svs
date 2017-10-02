from log import logger, setup_log
import curses
from widgets.log_widget import log_box
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
        try:
            curses.wrapper(self.start_ui)
        except Exception as e:
            self.stop()
            print e

    def start_ui(self, stdscr):
        stdscr.nodelay(1)
        maxy, maxx = stdscr.getmaxyx()
        begin_x = 2
        begin_y = maxy - 9
        height = 9
        width = maxx - 4

        # win.immedok(True)
        curses.setsyx(-1, -1)
        stdscr.addstr(0, 0, "Testing my curses app")
        stdscr.refresh()

        box2 = log_box(height, width, begin_y, begin_x)

        setup_log(box2)

        self.socket_server.start()

        logger.info("SSSS")

        box2.getch()
        self.stop()


    def stop(self):
        self.socket_server.stop()

        curses.curs_set(1)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

