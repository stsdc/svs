import logging
import curses
from socketserver import Server

import time
from network import HotSpot

from threading import Thread

class CursesHandler(logging.Handler):
    def __init__(self, screen):
        logging.Handler.__init__(self)
        self.screen = screen

    def emit(self, record):
        try:
            msg = self.format(record)
            screen = self.screen
            fs = "\n%s"
            screen.addstr(fs % msg.encode("UTF-8"))
            screen.refresh()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

logger = logging.getLogger('myLog')

class UI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.screen = None
        try:
            curses.wrapper(self.start_ui)
        except Exception as e:
            print e




    def setup_log(self, win):
        mh = CursesHandler(win)
        formatterDisplay = logging.Formatter('%(asctime)-8s|%(name)-12s|%(levelname)-6s|%(message)-s', '%H:%M:%S')
        mh.setFormatter(formatterDisplay)
        logger.addHandler(mh)

    def start_ui(self, stdscr):
        stdscr.nodelay(1)
        maxy, maxx = stdscr.getmaxyx()
        begin_x = 2
        begin_y = maxy - 5
        height = 5
        width = maxx - 4
        win = curses.newwin(height, width, begin_y, begin_x)
        win.border(0)
        curses.setsyx(-1, -1)
        stdscr.addstr("Testing my curses app")
        stdscr.refresh()
        win.refresh()
        win.scrollok(True)
        win.idlok(True)
        win.leaveok(True)

        self.setup_log(win)

        HotSpot()
        server = Server("", 50000)
        server.run()

        win.getch()

        curses.curs_set(1)
        curses.nocbreak()
        curses.echo()
        curses.endwin()





