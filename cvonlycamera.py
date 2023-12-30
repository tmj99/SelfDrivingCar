#!/usr/bin/python3

import cv2
import socket
import numpy as np
import time
import base64
from picamera2 import Picamera2

# configure camera
picam2 = Picamera2()
WIDTH = 680
HEIGHT = 480
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (WIDTH, HEIGHT)}))
picam2.start()

# UDP Client-Server interaction
host_ip = "192.168.0.48"
port = 8000
BUFF_SIZE = 65536

# configure socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

message = b'Hello'
client_socket.sendto(message,(host_ip,port))
packet, server_addr = client_socket.recvfrom(BUFF_SIZE)
print('packet received')

fps, st, frames_to_count, cnt = (0, 0, 20, 0)

# to track total frames
frame_no = 0

while True:
    im = picam2.capture_array()
    frame = im # cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    if frame.any():  # determine if there are any frames
        # new_height = int(frame.shape[0] * (WIDTH / frame.shape[1]))
        # resized_frame = cv2.resize(frame, (WIDTH, new_height))
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer)
        print(f'Packet size: {len(message)} | Frame shape: {frame.shape}')
        client_socket.sendto(message, server_addr)
        print(f'Video file sent | Frame Count: {frame_no}')
        
        # ------ not needed unless testing ------
        # frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # cv2.imshow('TRANSMITTING VIDEO', frame)
        # key = cv2.waitKey(1) & 0xFF
        # if key == ord('q'):
        #     client_socket.close()
        #     break
        
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1
        frame_no += 1
