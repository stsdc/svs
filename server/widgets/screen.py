import curses
from threading import Thread


class Screen(object):
    def __init__(self):
        self.maxx = None
        self.maxy = None

        self.run()

    def run(self):
        curses.wrapper(self.init_screen)

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