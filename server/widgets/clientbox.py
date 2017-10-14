from box import Box
import os
import threading


class ClientBox(Box):
    def __init__(self, h, w, y, x):
        super(ClientBox, self).__init__(h, w, y, x)

        self._thread = None

        self.title("Client-Unit0")

        self.add(4, 0, "ROTATION")
        self.add(5, 1, "X:")
        self.add(5, 7, "%16s" % "N/A")

    def update_data(self, data):
        rotx = data["rotation"]
        self.add(5, 7, "%16s" % rotx)
