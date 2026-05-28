from cv2 import aruco
# from cv2.typing import MatLike
import cv2
import numpy as np
import imutils

def get_obj_points():
    s = 100 # (mm)
    obj_points = np.array([
        [-s/2,  s/2, 0],
        [ s/2,  s/2, 0],
        [ s/2, -s/2, 0],
        [-s/2, -s/2, 0]
    ], dtype=np.float32)
    return obj_points

def calibrate():
    #* dummy camera matrix
    #! make sure to actually calibrate the camera eventually
    res = (1994, 2655)
    camera_mat = np.array([
        [res[0], 0, res[0]/2],
        [0, res[0], res[1]/2],
        [0, 0, 1]
    ])
    dist_coeffs = np.zeros((5, 1))
    return (camera_mat, dist_coeffs)

#corners[0]

def get_rvec_tvec(obj_points, img_points, camera_mat, dist_coeffs):
    success, rvec, tvec = cv2.solvePnP(obj_points, img_points, camera_mat, dist_coeffs)
    if not success:
        print("Uh Oh that failed")
        quit()
    # print(rvec) #* rotation vector
    # print(tvec) #* translation vector
    return (rvec, tvec)

def draw_axes(frame, camera_mat, dist_coeffs, rvec, tvec):
    #? pick a random number for marker_length??
    new_frame = cv2.drawFrameAxes(frame, camera_mat, dist_coeffs, rvec, tvec, 10)
    # new_frame = imutils.resize(new_frame, width=600)
    return new_frame
    # cv2.imshow("image", frame2)
    # cv2.waitKey(0)


image_path = "C:\\Users\\joshu\\OneDrive\\Documents\\Work\\Rovers\\Camera Scripts\\aruco_marker.png"

dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dict, params)

frame = cv2.imread(image_path)


camera_mat, dist_coeffs = calibrate()
obj_points = get_obj_points()

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    ret, frame = cam.read()
    
    corners, ids, rejected = detector.detectMarkers(frame)
    if len(corners) == 0:
        cv2.imshow("Image", frame)
    else:
        rvec, tvec = get_rvec_tvec(obj_points, corners[0], camera_mat, dist_coeffs)

        new_frame = draw_axes(frame, camera_mat, dist_coeffs, rvec, tvec)
        cv2.imshow("Image", new_frame)
    
    key = cv2.waitKey(1)
    # esc key
    if key & 0xFF == 27:
        print("esc")
        break