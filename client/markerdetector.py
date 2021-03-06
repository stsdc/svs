import os
from threading import Thread, Event

import cv2
import numpy as np
import yaml
from cv2 import aruco
from log import logger


# camera_matrix = np.array([[1776,0,762],[0,1780,1025],[0,0,1]],dtype=float)  #cx,cy ~= im.shape[1],im.shape[0]
# dist_coeffs = np.array([[0,0,0,0]],dtype=float) #need to be float type

class MarkerDetector(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self._stop_event = Event()

        self.PATH = "client/calibration.yml"
        self.MARKER_SIZE = 29

        self.camera_matrix = None
        self.dist_coeffs = None
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
        self.aruco_params = aruco.DetectorParameters_create()

        self.ids = []
        self.rotations = []
        self.translations = []

        self._calibrate()



    def run(self):
        captured = cv2.VideoCapture(0)
        while not self.stopped():
            # make it like in a good old movie
            gray = self._achromatise(captured)
            self.ids, self.rotations, self.translations = self._detect(gray)

    def _calibrate(self):
        try:
            calibration_file = open(self.PATH, "r")
            yml = yaml.load(calibration_file)
            self.camera_matrix = np.asanyarray(yml.get("camera_matrix"), dtype=float)
            self.dist_coeffs = np.asanyarray(yml.get("dist_coeffs"), dtype=float)
            if self.camera_matrix is None:
                logger.error("Calibrate error: Can't read camera matrix")
            elif self.dist_coeffs is None:
                logger.info("Calibrate error: Can't read distortion coefficients")
            else:
                logger.info("Calibrate: Loaded calibration file")
                logger.debug("Calibrate: Camera matrix: %s", yml.get("camera_matrix"))
                logger.debug("Calibrate: Distortion coefficients: %s", yml.get("dist_coeffs"))
        except (IOError) as e:
            logger.error('Calibrate error: %s', e)
            logger.error('If there is no calibration.yml try to run calibrate.py')

    def _achromatise(self, captured):
        ret, frame = captured.read()
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def _detect(self, gray):
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, self.aruco_dict, parameters=self.aruco_params)
        if type(ids) is np.ndarray:  # if aruco marker detected
            # self._log_markers(ids)

            rvec, tvec, _objPoints = aruco.estimatePoseSingleMarkers(
                corners, self.MARKER_SIZE, self.camera_matrix,
                self.dist_coeffs)
            return ids, rvec, tvec
        else:
            return [], [], []

    def _log_markers(self, ids):
        marker_string = ""
        for id in ids:
            marker_string += " " + str(id)
        logger.info("Marker(s) id:%s", marker_string)

    def get_marker(self):
        return (self.ids, self.rotations, self.translations)

    def stop(self):
        self._stop_event.set()
        self.join()
        logger.warning("Detector: Stopping...")

    def stopped(self):
        return self._stop_event.is_set()
