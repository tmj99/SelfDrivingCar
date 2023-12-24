from picamera2 import Picamera2
import numpy as np
import cv2 as cv
import time
picam2 = Picamera2()
"""figure out camera module"""

cap = cv.VideoCapture(picam2)

frame_number = 0

while cap.isOpened():
    ret, frame = cap.read()
    
    if ret == True:

        #  Test module
        cv.imshow('Frame', frame)

        # cv.imshow('Blurred', blur(frame))
        #cv.imshow('Original', frame)
        frame_number += 1
        print(frame_number)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()

cv.destroyAllWindows()


"""
This section is mainly for the controls of the car
"""

from Code.Server.Motor import *
PWM = Motor()

class speed:
    def __init__(self,speeds):
        self.frontleft = speeds[0]
        self.rearleft = speeds[1]
        self.frontright = speeds[2]
        self.rearright = speeds[3]

    def accelerate(self, speeds):
        speeds[0] += 1000
        speeds[1] += 1000
        speeds[2] += 1000
        speeds[3] += 1000

    def deccelerate(self, speeds):
        speeds[0] -= 1000
        speeds[1] -= 1000
        speeds[2] -= 1000
        speeds[3] -= 1000

    def roleft(self, speeds):
        speeds[2] += 1000
        speeds[3] += 1000

    def roright(self, speeds):
        speeds[0] += 1000
        speeds[1] += 1000


""" remember to call destroy() to stop the vehicle before breaking """