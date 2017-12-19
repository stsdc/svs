from box import Box
import os


# import threading


class ClientBox(Box):
    def __init__(self, h, w, y, x, title="Client"):
        super(ClientBox, self).__init__(h, w, y, x)

        # self._thread = None

        self.title(title)

        self.add(1, 5, "TOP MARKER ID: ", self.bold)

        self.rot_pos_x_A = 0
        self.rot_pos_y_A = 2

        self.tran_pos_x_A = 0
        self.tran_pos_y_A = 7

        self.add(self.rot_pos_y_A, self.rot_pos_x_A, "ROTATION")
        self.xyz_data_template(self.rot_pos_y_A, self.rot_pos_x_A, None)

        self.add(self.tran_pos_y_A, self.tran_pos_x_A, "TRANSLATION [MM]")
        self.xyz_data_template(self.tran_pos_y_A, self.tran_pos_x_A, None)

        self.add(1, 28, "SIDE MARKER ID: ", self.bold)

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
        if len(data) != 0:
            for marker in data:
                if marker["id"] == 9:
                    self.show_marker_A_data(marker)
                elif marker["id"] == 16:
                    self.show_marker_B_data(marker)

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

    def show_marker_A_data(self, marker):
        self.add(1, 5, "TOP MARKER ID: %d" % marker["id"], self.bold)
        self.xyz_data_template(self.rot_pos_y_A, self.rot_pos_x_A, marker["rot"])
        self.xyz_data_template(self.tran_pos_y_A, self.tran_pos_x_A, marker["tran"])

    def show_marker_B_data(self, marker):
        self.add(1, 28, "SIDE MARKER ID: %d" % marker["id"], self.bold)
        self.xyz_data_template(self.rot_pos_y_B, self.rot_pos_x_B, marker["rot"])
        self.xyz_data_template(self.tran_pos_y_B, self.tran_pos_x_B, marker["tran"])
