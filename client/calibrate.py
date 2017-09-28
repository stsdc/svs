import sys
from threading import Thread

import cv2
import cv2.aruco as aruco
import numpy as np
import yaml


class Calibrate(object):

    def __init__(self):
        self.dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        square_length = 40
        marker_length = 30
        rows = 7
        columns = 5
        self.board = aruco.CharucoBoard_create(
            columns, rows, square_length, marker_length, self.dict)
        self.all_ch_corners = []  # all Charuco Corners
        self.all_ch_ids = []  # all Charuco Ids
        self.img_size = []

        self.filename = "calibration.yml"

        video = Video()
        video.start()
        print [video.img]
        try:
            while not video.img:
                continue
        except ValueError as e:
            print e
            self.take_pictures(video.img)
            self.start()

    def take_pictures(self, img):
        decimator = 0
        print "Press space to capture picture"
        for i in range(30):
            if cv2.waitKey(0):
                print "reading %s" % i
                [markerCorners, markerIds, rejectedImgPoints] = cv2.aruco.detectMarkers(img, self.dict)

                if len(markerCorners) > 0:
                    [ret, ch_corners, ch_ids] = cv2.aruco.interpolateCornersCharuco(
                        markerCorners, markerIds, img, self.board)
                    if ch_corners is not None and ch_ids is not None and len(ch_corners) > 3 and decimator % 3 == 0:
                        self.all_ch_corners.append(ch_corners)
                        self.all_ch_ids.append(ch_ids)

                decimator += 1
        self.img_size = img.shape

    def start(self):
        try:
            [ret, cam_matrix, dist_coeffs, rvecs, tvecs] = cv2.aruco.calibrateCameraCharuco(
                self.all_ch_corners, self.all_ch_ids, self.board, self.img_size, None, None)
            print "Rep Error:", ret
            self.saveCameraParams(cam_matrix, dist_coeffs, ret)

        except ValueError as e:
            print(e)
        except NameError as e:
            print(e)
        except AttributeError as e:
            print(e)
        except:
            print "calibrateCameraCharuco fail:", sys.exc_info()[0]

    def saveCameraParams(self, cam_matrix, dist_coeffs, ret):
        print(cam_matrix)

        calib_data = dict(
            image_width=self.img_size[0],
            image_height=self.img_size[1],
            camera_matrix=cam_matrix.tolist(),
            dist_coeffs=dist_coeffs.tolist(),
            avg_reprojection_error=ret,
        )

        with open(self.filename, 'w') as outfile:
            yaml.dump(calib_data, outfile)


class Video(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.img = []

    def run(self):
        print "Starting video"
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            self.img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            smallimg = cv2.resize(self.img, (320, 240))
            cv2.imshow("Calibration", smallimg)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

Calibrate()
# Video().start()
