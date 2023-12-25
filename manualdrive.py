# from picamera2 import Picamera2
# import numpy as np
# import cv2 as cv
# import time

# picam2 = Picamera2()
# """figure out camera module"""

# cap = cv.VideoCapture(picam2)

# frame_number = 0

# while cap.isOpened():
#     ret, frame = cap.read()
    
#     if ret == True:

#         #  Test module
#         cv.imshow('Frame', frame)

#         # cv.imshow('Blurred', blur(frame))
#         #cv.imshow('Original', frame)
#         frame_number += 1
#         print(frame_number)

#     if cv.waitKey(1) == ord('q'):
#         break

# cap.release()

# cv.destroyAllWindows()


"""
This section is mainly for the controls of the car
"""

from Motor import *

PWM = Motor()

def start_session():

    speeds = [100,100,100,100]

    try:
        while True:
            PWM.setMotorModel(speeds[0],speeds[1],speeds[2],speeds[3])
            print("Speed of:",speeds)

    except KeyboardInterrupt:
        PWM.setMotorModel(0,0,0,0)
        print ("\nEnd of program")
        return

start_session()