from log import CursesHandler, logger
import logging
import curses
from threading import Thread
from widgets import Screen, StatusBar, CommandBar, TitleBar, TextPanel, TabPanel

class Window(Screen):
    def __init__(self, win):
        super(Window, self).__init__(win)

        self.title = TitleBar(self)

        self.main = TextPanel(self)

        self.status = StatusBar(self)
        self.command = CommandBar(self)

        self.redraw()

    def set_title(self, text):
        self.title.set_text(text)

    def set_status(self, text):
        self.status.set_text(text)

    def run(self):
        curses.curs_set(0)
        while True:
            c = self.command.get_char()
            if c == 'q':
                break

class UI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        curses.wrapper(self.start_ui)

    def start_ui(self, stdscr):
        screen = Window(stdscr)

        screen.set_title('%s v%s' % ("TEST", "0.1"))
        screen.set_status('Standby ready')

        screen.refresh()

        screen.run()
        handler = CursesHandler(screen)
        formatterDisplay = logging.Formatter('%(asctime)-8s|%(name)-12s|%(levelname)-6s|%(message)-s', '%H:%M:%S')
        handler.setFormatter(formatterDisplay)
        logger.addHandler(handler)
        logger.info("SKS")
