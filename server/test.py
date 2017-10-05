# from log import logger
from time import sleep

# def testy():
#     for i in range(10):
#         logger.info('message %i', i)
#         logger.debug('message %i', i)
#         logger.warning('message %i', i)
#         sleep(1)
import curses

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    try:
        for i in range(0, 255):
            stdscr.addstr(str(i) + " ", curses.color_pair(i))
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.getch()

curses.wrapper(main)