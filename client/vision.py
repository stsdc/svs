import os

import cv2
import numpy as np
from cv2 import aruco

# calibrationFile = "../calibration.yml"
# calibrationParams = cv2.FileStorage(calibrationFile, cv2.FILE_STORAGE_READ)
# print calibrationParams.getNode("cameraMatrix")
# camera_matrix = calibrationParams.getNode("camera_matrix").getNode("data").mat()
# print camera_matrix
# dist_coeffs = calibrationParams.getNode("distortion_coefficients").mat()

camera_matrix = np.array([[1776,0,762],[0,1780,1025],[0,0,1]],dtype=float)  #cx,cy ~= im.shape[1],im.shape[0]
dist_coeffs = np.array([[0,0,0,0]],dtype=float) #need to be float type

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_1000)
arucoParams = aruco.DetectorParameters_create()
markerLength = 35.5  # Here, I'm using centimetre as a unit.

cap = cv2.VideoCapture(0)


while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        gray, aruco_dict, parameters=arucoParams)  # Detect aruco
    if ids != None:  # if aruco marker detected
        print(ids)
        rvec, tvec, _objPoints = aruco.estimatePoseSingleMarkers(corners, markerLength, camera_matrix, dist_coeffs)  # For a single marker
        imgWithAruco = aruco.drawDetectedMarkers(gray, corners,
                                                 ids, (0, 255, 0))
        imgWithAruco = aruco.drawAxis(
            imgWithAruco, camera_matrix, dist_coeffs, rvec, tvec, 100
        )  # axis length 100 can be changed according to your requirement
    else:  # if aruco marker is NOT detected
        imgWithAruco = gray  # assign imRemapped_color to imgWithAruco directly
    cv2.imshow("aruco", imgWithAruco)  # display
    if cv2.waitKey(2) & 0xFF == ord('q'):  # if 'q' is pressed, quit.
        break
