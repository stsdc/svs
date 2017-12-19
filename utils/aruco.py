import numpy as np
import cv2
import cv2.aruco as aruco


cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480);
camera_matrix = np.array([[1776,0,762],[0,1780,1025],[0,0,1]],dtype=float)
dist_coeffs = np.array([[0,0,0,0]],dtype=float)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    #print(frame.shape) #480x640
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
    parameters =  aruco.DetectorParameters_create()

    #print(parameters)

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
        #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print(ids)

    #It's working.
    # my problem was that the cellphone put black all around it. The alrogithm
    # depends very much upon finding rectangular black blobs
    colored = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    colored = aruco.drawDetectedMarkers(colored, corners, ids)

    rvecs, tvecs, objpoints = aruco.estimatePoseSingleMarkers(corners, 30, camera_matrix, dist_coeffs)

    if rvecs:
        for i in range(len(rvecs)):
            gray = aruco.drawAxis(colored, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], 30)

    #print(rejectedImgPoints)
    # Display the resulting frame
    cv2.imshow('Marker detection', colored)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
