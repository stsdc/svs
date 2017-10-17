from box import Box
import os
import threading


class ClientBox(Box):
    def __init__(self, h, w, y, x):
        super(ClientBox, self).__init__(h, w, y, x)

        self._thread = None

        self.title("Client-Unit0")

        self.rot_pos_x = 0
        self.rot_block_y = 2

        self.tran_pos_x = 0
        self.tran_pos_y = 7

        self.add(self.rot_block_y, self.rot_pos_x, "ROTATION")
        self.xyz_data_template(self.rot_block_y, self.rot_pos_x, None)

        self.add(self.tran_pos_y, self.tran_pos_x, "TRANSLATION")
        self.xyz_data_template(self.tran_pos_y, self.tran_pos_x, None)

    def update_data(self, data):
        self.xyz_data_template(self.rot_block_y, self.rot_pos_x, data["rotation"])
        self.xyz_data_template(self.tran_pos_y, self.tran_pos_x, data["translation"])

    def xyz_data_template(self, pos_y, pos_x, data):
        self.add(pos_y + 1, 1, "X:")
        self.add(pos_y + 2, 1, "Y:")
        self.add(pos_y + 3, 1, "Z:")
        pos_x = pos_x + 4
        if data:
            self.add(pos_y + 1, pos_x, "%19s" % data[0])
            self.add(pos_y + 2, pos_x, "%19s" % data[1])
            self.add(pos_y + 3, pos_x, "%19s" % data[2])
        else:
            self.add(pos_y + 1, pos_x, "%19s" % "N/A")
            self.add(pos_y + 2, pos_x, "%19s" % "N/A")
            self.add(pos_y + 3, pos_x, "%19s" % "N/A")
