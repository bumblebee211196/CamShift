"""
track.py: A simple application to track objects in videos or via webcam using python and open-cv.
"""

__author__ = "S Sathish Babu"
__date__   = "22-12-2020 Saturday 17:30"
__email__  = "bumblebee211196@gmail.com"

import cv2
import numpy as np

frame = None
input_mode = False
roi_points = []


def select_roi(event, x, y, flags, param):
    """Method to get the object coordinates"""
    global frame, input_mode, roi_points
    if input_mode and event == cv2.EVENT_LBUTTONDOWN and len(roi_points) < 4:
        roi_points.append((x, y))
        cv2.circle(frame, (x, y), 3, (0, 255, 0), 2)
        cv2.imshow('Output', frame)


vc = cv2.VideoCapture(0)
cv2.namedWindow('Output')
cv2.setMouseCallback('Output', select_roi)
roi_box = None

while True:
    _, frame = vc.read()
    if roi_box:
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        back_projection = cv2.calcBackProject([frame_hsv], [0], roi_hist, [0, 180], 1)
        pts, track_window = cv2.CamShift(back_projection, roi_box,
                                         (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))
        pts = np.int0(cv2.boxPoints(pts))
        cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
    cv2.imshow('Output', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('i') and len(roi_points) < 4:
        input_mode = True
        original = frame.copy()
        while len(roi_points) < 4:
            cv2.imshow('Output', frame)
            cv2.waitKey(0)
        roi_points = np.array(roi_points)
        total = roi_points.sum(axis=1)
        tl = roi_points[np.argmin(total)]
        br = roi_points[np.argmax(total)]
        roi = original[tl[1]:br[1], tl[0]:br[0]]
        roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        roi_hist = cv2.calcHist([roi_hsv], [0], None, [180], [0, 180])
        roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
        roi_box = (tl[0], tl[1], br[0], br[1])
    elif key == ord('q'):
        break

vc.release()
cv2.destroyAllWindows()
