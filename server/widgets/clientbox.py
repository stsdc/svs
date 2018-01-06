from box import Box
import cv2
import numpy as np
from log import logger
# import threading
import math

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

        self.add(self.rot_pos_y_A, self.rot_pos_x_A, "ROTATION [DEG]")
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
                if marker["id"] == 1: #9
                    self.show_marker_A_data(marker)
                elif marker["id"] == 2: # 16
                    self.show_marker_B_data(marker)

    def xyz_data_template(self, pos_y, pos_x, data):
        self.add(pos_y + 1, 1, "X:")
        self.add(pos_y + 2, 1, "Y:")
        self.add(pos_y + 3, 1, "Z:")
        pos_x = pos_x + 4

        if data:
            tranx = round(data[0])
            trany = round(data[1])
            tranz = round(data[2])

            self.add(pos_y + 1, pos_x, "%19d" % tranx)
            self.add(pos_y + 2, pos_x, "%19d" % trany)
            self.add(pos_y + 3, pos_x, "%19d" % tranz)
        else:
            self.add(pos_y + 1, pos_x, "%19s" % "N/A")
            self.add(pos_y + 2, pos_x, "%19s" % "N/A")
            self.add(pos_y + 3, pos_x, "%19s" % "N/A")

    def xyz_data_template_rot(self, pos_y, pos_x, data):
        self.add(pos_y + 1, 1, "X:")
        self.add(pos_y + 2, 1, "Y:")
        self.add(pos_y + 3, 1, "Z:")
        pos_x = pos_x + 4

        R = cv2.Rodrigues(np.array(data))[0]
        euler = rotationMatrixToEulerAngles(R)

        rotx = round(euler[0] * 180 / 3.14)
        roty = round(euler[1] * 180 / 3.14)
        rotz = round(euler[2] * 180 / 3.14)

        if data:
            self.add(pos_y + 1, pos_x, "%19d" % self.rot_lol(rotx))
            self.add(pos_y + 2, pos_x, "%19d" % roty)
            self.add(pos_y + 3, pos_x, "%19d" % rotz)
        else:
            self.add(pos_y + 1, pos_x, "%19s" % "N/A")
            self.add(pos_y + 2, pos_x, "%19s" % "N/A")
            self.add(pos_y + 3, pos_x, "%19s" % "N/A")

    def show_marker_A_data(self, marker):
        self.add(1, 5, "TOP MARKER ID: %d" % marker["id"], self.bold)
        self.xyz_data_template_rot(self.rot_pos_y_A, self.rot_pos_x_A, marker["rot"])
        self.xyz_data_template(self.tran_pos_y_A, self.tran_pos_x_A, marker["tran"])

    def show_marker_B_data(self, marker):
        self.add(1, 28, "SIDE MARKER ID: %d" % marker["id"], self.bold)
        self.xyz_data_template_rot(self.rot_pos_y_B, self.rot_pos_x_B, marker["rot"])
        self.xyz_data_template(self.tran_pos_y_B, self.tran_pos_x_B, marker["tran"])

    def rot_lol(self, rotx):
        if rotx < 0:
            return 180 + rotx
        return rotx - 180


# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R):
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])