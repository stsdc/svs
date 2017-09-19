import numpy as np
import cv2
import cv2.aruco as aruco
import argparse
import sys
import yaml
import numpy as np

dictionary = aruco.Dictionary_get(aruco.DICT_6X6_250)

# * The first and second parameters are the number of squares in X
# and Y direction respectively.
# * The third and fourth parameters are the length of the squares and
# the markers respectively. They can be provided in any unit, having
# in mind that the estimated pose for this board would be measured
# in the same units (usually meters are used).
board = aruco.CharucoBoard_create(5, 7, 0.04, 0.02, dictionary)

# The first parameter is the size of the output image in pixels.
# In this case 600x500 pixels. If this is not proportional to the
# board dimensions, it will be centered on the image.
#
# The second parameter is the (optional) margin in pixels, so none
# of the markers are touching the image border. In this case the
# margin is 10.
#
# Finally, the size of the marker border, similarly to drawMarker()
# function. The default value is 1.

def saveCameraParams(filename,imageSize,cameraMatrix,distCoeffs,totalAvgErr):

   print(cameraMatrix)

   calibration = {'camera_matrix': cameraMatrix.tolist(),'dist_coeffs': distCoeffs.tolist()}

   calibrationData = dict(
       image_width = imageSize[0],
       image_height = imageSize[1],
       camera_matrix = dict(
         data = cameraMatrix.tolist(),
         ),
       distortion_coefficients = dict(
           data = disCoeffs.tolist(),
           ),
       avg_reprojection_error = totalAvgErr,
   )

   with open(filename,'w') as outfile:
       yaml.dump(calibrationData,outfile)


parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", help="ouput calibration filename",default="calibration.yml")
parser.add_argument("-s", "--size", help="size of squares in meters",type=float, default="0.035")
args = parser.parse_args()

sqWidth = 12 #number of squares width
sqHeight = 8 #number of squares height
allCorners = [] #all Charuco Corners
allIds = [] #all Charuco Ids
decimator = 0
#cameraMatrix = np.array([])
#disCoeffs = np.array([])
cap = cv2.VideoCapture(0)

for i in range(30):
    print "reading %s" % i
    ret,frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    [markerCorners,markerIds,rejectedImgPoints] = cv2.aruco.detectMarkers(img,dictionary)

    if len(markerCorners)>0:
        [ret,charucoCorners,charucoIds] = cv2.aruco.interpolateCornersCharuco(markerCorners,markerIds,img,board)
        if charucoCorners is not None and charucoIds is not None and len(charucoCorners)>3 and decimator%3==0:
            allCorners.append(charucoCorners)
            allIds.append(charucoIds)

        cv2.aruco.drawDetectedMarkers(img,markerCorners,markerIds)
        cv2.aruco.drawDetectedCornersCharuco(img,charucoCorners,charucoIds)

        #for corner in allCorners:
        #    cv2.circle(img,(corner[0][0], corner[0][0]),50,(255,255,255))

    smallimg = cv2.resize(img,(1024,768))
    cv2.imshow("frame",smallimg)
    cv2.waitKey(0) #any key
    decimator+=1

imsize = img.shape
print(imsize)
#try Calibration
try:
    [ret,cameraMatrix,disCoeffs,rvecs,tvecs] = cv2.aruco.calibrateCameraCharuco(allCorners,allIds,board,imsize,None,None)
    print "Rep Error:" ,ret
    #np.savez(args.file,ret=ret,mtx=cameraMatrix,dist=disCoeffs,rvecs=rvecs,tvecs=tvecs)
    saveCameraParams(args.file,imsize,cameraMatrix,disCoeffs,ret)

except ValueError as e:
    print(e)
except NameError as e:
    print(e)
except AttributeError as e:
    print(e)
except:
    print "calibrateCameraCharuco fail:" , sys.exc_info()[0]

print "Press any key on window to exit"
cv2.waitKey(0) #any key
cv2.destroyAllWindows()
