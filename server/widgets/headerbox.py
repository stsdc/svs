from box import Box


class HeaderBox(Box):
    def __init__(self, h, w, y, x):
        super(HeaderBox, self).__init__(h, w, y, x)
        self.set_colors_scheme()
        text = "Synergia Vision System"
        self.window.addstr(0, (w / 2) - len(text) / 2, text, self.bold)
        self.refresh()
