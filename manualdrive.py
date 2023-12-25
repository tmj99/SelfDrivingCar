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
import pygame

pygame.init()
screen = pygame.display.set_mode((100,100))

PWM = Motor()

def accelerate(speed):
    speed = [number + 500 for number in speed]
    print("Accelerate ...")

def deccelerate(speed):
    speed = [number - 500 for number in speed]
    print("Deccelerate ...")

def roleft(speed):
    speed[0] -= 500
    speed[1] -= 500
    speed[3] += 500
    speed[4] += 500
    print("Rotate left ...")

def roright(speed):
    speed[0] += 500
    speed[1] += 500
    speed[3] -= 500
    speed[4] -= 500
    print("Rotate right ...")

def start_session():

    speeds = [0,0,0,0]

    try:
        while True:
            PWM.setMotorModel(speeds[0],speeds[1],speeds[2],speeds[3])
            time.sleep(1)
            print("Speed of:",speeds)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        accelerate(speeds)
                    
                    elif event.key == pygame.K_s:
                        deccelerate(speeds)
                    
                    elif event.key == pygame.K_a:
                        roleft(speeds)
                    
                    elif event.key == pygame.K_d:
                        roright(speeds)
                    
                    elif event.key == pygame.K_q:
                        PWM.setMotorModel(0,0,0,0)
                        print("Quiting ...")
                        return

    except KeyboardInterrupt:
        PWM.setMotorModel(0,0,0,0)
        print ("\nEnd of program")
        return

start_session()