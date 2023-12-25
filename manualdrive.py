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

def forward():
    PWM.setMotorModel(1000,1000,1000,1000)
    print("Forward ...")
    time.sleep(0.75)
    PWM.setMotorModel(0,0,0,0)

def backward(speed):
    PWM.setMotorModel(-1000,-1000,-1000,-1000)
    print("Backward ...")
    time.sleep(0.75)
    PWM.setMotorModel(0,0,0,0)

def roleft(degree):
    PWM.Rotate(degree)
    print("Rotating {} degrees to the left ... ".format(degree))
    PWM.setMotorModel(0,0,0,0)

def roright(degree):
    PWM.Rotate(-degree)
    print("Rotating {} degrees to the left ... ".format(degree))
    PWM.setMotorModel(0,0,0,0)

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
                        forward()
                    
                    elif event.key == pygame.K_s:
                        backward()
                    
                    elif event.key == pygame.K_a:
                        roleft(45)
                    
                    elif event.key == pygame.K_d:
                        roright(45)
                    
                    elif event.key == pygame.K_q:
                        PWM.setMotorModel(0,0,0,0)
                        print("Quiting ...")
                        return

    except KeyboardInterrupt:
        PWM.setMotorModel(0,0,0,0)
        print ("\nEnd of program")
        return

start_session()