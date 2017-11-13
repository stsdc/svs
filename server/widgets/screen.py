import curses
# from threading import Thread


class Screen(object):
    def __init__(self):
        self.maxx = None
        self.maxy = None
        self.stdscr = None
        self.run()

    def run(self):
        curses.wrapper(self.init_screen)

    def init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

    def init_screen(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        curses.flushinp()
        stdscr.nodelay(1)
        stdscr.keypad(1)
        self.maxy, self.maxx = stdscr.getmaxyx()
        curses.setsyx(-1, -1)
        stdscr.refresh()
        self.init_colors()
        curses.noecho()


    def stop(self):
        curses.curs_set(1)
        curses.nocbreak()
        # curses.echo()
        curses.endwin()

    def refresh(self):
        self.stdscr.refresh()
