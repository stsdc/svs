from box import Box
import os
import threading


class ClientBox(Box):
    def __init__(self, h, w, y, x):
        super(ClientBox, self).__init__(h, w, y, x)

        self._thread = None

        self.title("Client-Unit0")

        self.rot_b_x = 0
        self.rot_b_x_right = self.rot_b_x+4
        self.rot_block_y = 2
        self.add(self.rot_block_y, self.rot_b_x, "ROTATION")
        self.add(self.rot_block_y+1, self.rot_b_x+1, "X:")
        self.add(self.rot_block_y+1, self.rot_b_x_right, "%19s" % "N/A")

        self.add(self.rot_block_y+2, self.rot_b_x+1, "Y:")
        self.add(self.rot_block_y+2, self.rot_b_x_right, "%19s" % "N/A")
        #
        self.add(self.rot_block_y+3, self.rot_b_x+1, "Z:")
        self.add(self.rot_block_y+3, self.rot_b_x_right, "%19s" % "N/A")

    def update_data(self, data):
        if data["rotation"]:
            self.add(self.rot_block_y+1, self.rot_b_x_right, "%19s" % data["rotation"][0])
            self.add(self.rot_block_y+2, self.rot_b_x_right, "%19s" % data["rotation"][1])
            self.add(self.rot_block_y+3, self.rot_b_x_right, "%19s" % data["rotation"][2])
        else:
            self.add(self.rot_block_y+1, self.rot_b_x_right, "%19s" % "N/A")
            self.add(self.rot_block_y+2, self.rot_b_x_right, "%19s" % "N/A")
            self.add(self.rot_block_y+3, self.rot_b_x_right, "%19s" % "N/A")