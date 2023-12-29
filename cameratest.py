#!/usr/bin/python3
import os
import socket
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput

# Configuring the camera and encoder
picam2 = Picamera2()
video_config = picam2.create_video_configuration({"size": (640, 480)})
picam2.configure(video_config)
encoder = H264Encoder(1000000)

# UDP Client-Server interaction
UDP_IP          = "192.168.0.48"
UDP_PORT        = 8000
BufferSize      = 65536

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    udp_socket.connect((UDP_IP, UDP_PORT))
    stream = udp_socket.makefile("wb")
    print(stream)

    # Encoder outputs
    output1 = FileOutput(stream)
    output2 = FileOutput()
    encoder.output = [output1, output2]

    # Start streaming to the network.
    picam2.start_encoder(encoder)
    picam2.start()
    time.sleep(5)

    # Start recording to a file.
    # output2.fileoutput = "test.h264"
    # print("Recording to file in progress.")
    # output2.start()
    # time.sleep(5)
    # output2.stop()
    # print("Recording stopped.")

    # The file is closed, but carry on streaming to the network.
    time.sleep(9999999)