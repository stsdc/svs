import curses
import logging
import coloredlogs
import os

os.environ['COLOREDLOGS_LOG_FORMAT'] ='%(asctime)s.%(msecs)03d %(name)s - %(message)s'
os.environ['COLOREDLOGS_DATE_FORMAT'] ='%H%M%S'

logger = logging.getLogger("Test")

coloredlogs.install(level='DEBUG')

class CursesHandler(logging.Handler):
    def __init__(self, win, level=logging.DEBUG):
        logging.Handler.__init__(self, level)
        self.win = win

    def emit(self, record):
        self.win.addstr(record.getMessage())
        self.win.refresh()

def main(scrn):

    handler = CursesHandler(scrn.subwin(5,80, 19,0))
    logger.addHandler(handler)

    win = scrn.subwin(10,80, 0,0)

    for i in range(0,10):
        curses.delay_output(250)
        logger.info("Now i = %s", i)
    win.getch()


if __name__ == "__main__":
    curses.wrapper(main)
