from log import logger, setup_log
import curses
# import test
from time import sleep
from socketserver import SocketServer
from threading import Thread


class UI():
    def __init__(self):
        # Thread.__init__(self)
        # self.daemon = True
        self.screen = None
        try:
            curses.wrapper(self.start_ui)
        except Exception as e:
            print e

    def start_ui(self, stdscr):
        stdscr.nodelay(1)
        maxy, maxx = stdscr.getmaxyx()
        begin_x = 2
        begin_y = maxy - 9
        height = 9
        width = maxx - 4
        win = curses.newwin(height, width, begin_y, begin_x)

        # win.immedok(True)
        curses.setsyx(-1, -1)
        stdscr.addstr(0, 0, "Testing my curses app")
        stdscr.refresh()
        win.box()
        win.addstr(1, 1, "Testing my curses app")
        box2 = win.derwin(height - 2, width - 2, 1, 1)
        win.refresh()
        box2.refresh()
        box2.scrollok(True)
        box2.idlok(True)
        box2.leaveok(True)

        setup_log(box2)

        socket_server = SocketServer("", 8888)
        socket_server.start()

        logger.info("SSSS")

        win.getch()

        curses.curs_set(1)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
