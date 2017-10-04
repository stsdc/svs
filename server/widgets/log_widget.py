import curses
from box import Box
from log import setup_log


class LogBox(Box):
    def __init__(self, h, w, y, x):
        super(LogBox, self).__init__(h, w, y, x)
        setup_log(self.box)
