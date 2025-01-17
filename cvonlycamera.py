#!/usr/bin/python3

import cv2
import socket
import numpy as np
import time
import base64
from picamera2 import Picamera2

# configure camera
picam2 = Picamera2()
WIDTH = 1280
HEIGHT = 720
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

# initialize packet size
packet_size = 60000

def send_packet(packet_data, packet_number):
    client_socket.sendto(packet_data, server_addr)
    print(f'Packet {packet_number} size: {len(packet_data)} sent')

def split_and_send_image(frame):
    encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    message = base64.b64encode(buffer)
    total_packets = (len(message) + packet_size - 1) // packet_size
    print(f'Total vid size: { len(message) } | Frame Count: {frame_no}')
    for i in range(total_packets):
        start_idx = i * packet_size
        end_idx = start_idx + packet_size
        packet_data = message[start_idx:end_idx]
        send_packet(packet_data, i)

while True:
    im = picam2.capture_array()
    #frame = im  cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    if im.any():  # determine if there are any frames
        split_and_send_image(im)
        
        # ------ not needed unless testing ------
        # frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # cv2.imshow('TRANSMITTING VIDEO', frame)
        # key = cv2.waitKey(1) & 0xFF
        # if key == ord('q'):
        #     client_socket.close()
        #     break
        # ------ for frame counting ------
        # if cnt == frames_to_count:
        #     try:
        #         fps = round(frames_to_count / (time.time() - st))
        #         st = time.time()
        #         cnt = 0
        #     except:
        #         pass
        # cnt += 1
        frame_no += 1
