# Create a logger object.
import logging
import coloredlogs
import os
import curses

# os.environ['COLOREDLOGS_LOG_FORMAT'] = '%(asctime)s.%(msecs)03d %(name)s - %(message)s'
# os.environ['COLOREDLOGS_DATE_FORMAT'] = '%H%M%S'

logger = logging.getLogger("SVSystem")


# coloredlogs.install(level='DEBUG')


# Some examples.
# logger.debug("this is a debugging message")
# logger.info("this is an informational message")
# logger.warn("this is a warning message")
# logger.error("this is an error message")
# logger.critical("this is a critical message")

class CursesHandler(logging.Handler):
    def __init__(self, screen, level=logging.DEBUG):
        logging.Handler.__init__(self, level)
        self.screen = screen

    def emit(self, record):
        try:
            attr = {"DEBUG": curses.A_NORMAL,
                    "INFO": curses.A_NORMAL,
                    "WARNING": curses.A_BOLD,
                    "ERROR": curses.A_BOLD,
                    "CRITICAL": curses.A_STANDOUT}
            screen = self.screen
            msg = self.format(self.format(record))
            screen.addstr(self.format(record))
            screen.main.refresh()
        except:
            self.handleError(record)
