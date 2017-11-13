from box import Box
import os


# import threading


class ClientBox(Box):
    def __init__(self, h, w, y, x, title="Client"):
        super(ClientBox, self).__init__(h, w, y, x)

        # self._thread = None

        self.title(title)

        self.add(1, 7, "MARKER A", self.bold)

        self.rot_pos_x_A = 0
        self.rot_pos_y_A = 2

        self.tran_pos_x_A = 0
        self.tran_pos_y_A = 7

        self.add(self.rot_pos_y_A, self.rot_pos_x_A, "ROTATION")
        self.xyz_data_template(self.rot_pos_y_A, self.rot_pos_x_A, None)

        self.add(self.tran_pos_y_A, self.tran_pos_x_A, "TRANSLATION [MM]")
        self.xyz_data_template(self.tran_pos_y_A, self.tran_pos_x_A, None)

        self.add(1, 31, "MARKER B", self.bold)

        self.rot_pos_x_B = 24
        self.rot_pos_y_B = 2

        self.tran_pos_x_B = 24
        self.tran_pos_y_B = 7

        # self.add(self.rot_pos_y_B, self.rot_pos_x_B, "ROTATION")
        self.xyz_data_template(self.rot_pos_y_B, self.rot_pos_x_B, None)

        # self.add(self.tran_pos_y_B, self.tran_pos_x_B, "TRANSLATION")
        self.xyz_data_template(self.tran_pos_y_B, self.tran_pos_x_B, None)
        self.set_colors_scheme()

    def update_data(self, data):
        # should make for loop or assign markers to variables
        if len(data) == 1:
            self.add(1, 7, "MARKER %d" % data[0]["id"], self.bold)
            self.xyz_data_template(self.rot_pos_y_A, self.rot_pos_x_A, data[0]["rot"])
            self.xyz_data_template(self.tran_pos_y_A, self.tran_pos_x_A, data[0]["tran"])

            # if len(data) == 2:
            #     self.add(1, 7, "MARKER %d" % data[1]["id"], self.bold)
            #     self.xyz_data_template(self.rot_pos_y_A, self.rot_pos_x_A, data[0]["rot"])
            #     self.xyz_data_template(self.tran_pos_y_A, self.tran_pos_x_A, data[0]["tran"])

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
