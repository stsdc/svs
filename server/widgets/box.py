import curses


class Box(object):
    def __init__(self, h, w, y, x):
        self.h = h
        self.w = w
        self.window = curses.newwin(h, w, y, x)
        self.box = None

        # Style properties
        self.bold = curses.A_BOLD

    def wrap(self, h, w):
        self.window.box()
        self.box = self.window.derwin(h - 2, w - 2, 1, 1)
        self.box.scrollok(True)
        self.box.idlok(True)
        self.box.leaveok(True)
        self.refresh()


    def refresh(self):
        self.window.refresh()
        if self.box:
            self.box.refresh()

    def title(self, text):
        self.wrap(self.h, self.w)
        self.window.addstr(0, 2, text)
        self.refresh()

    def set_colors_scheme(self):
        curses.init_pair(44, 43, 0)
        self.window.bkgd(' ', curses.color_pair(44))

    def add(self, line_y, line_x, text, style = curses.A_NORMAL):
        self.box.addstr(line_y, line_x, text, style)
        self.refresh()
