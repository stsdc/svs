import curses


class Box(object):
    def __init__(self, h, w, y, x):
        wrapper = curses.newwin(h, w, y, x)
        wrapper.box()
        wrapper.addstr(0, 2, "Logs")
        self.box = wrapper.derwin(h - 2, w - 2, 1, 1)
        wrapper.refresh()
        self.box.refresh()
        self.box.scrollok(True)
        self.box.idlok(True)
        self.box.leaveok(True)
