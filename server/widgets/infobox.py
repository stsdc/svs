from box import Box


class InfoBox(Box):
    def __init__(self, h, w, y, x):
        super(InfoBox, self).__init__(h, w, y, x)
        self.title("Server - Main Unit")
