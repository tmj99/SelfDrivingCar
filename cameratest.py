#!/usr/bin/python3

import socket
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput

picam2 = Picamera2()
video_config = picam2.create_video_configuration({"size": (1280, 720)})
picam2.configure(video_config)
encoder = H264Encoder(1000000)

# UDP Client-Server interaction
UDP_IP          = "192.168.0.48"
UDP_PORT        = 8000
buffersize      = 1024

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.connect((UDP_IP, UDP_PORT))
    stream = sock.makefile("wb")

output1 = FileOutput(stream)
output2 = FileOutput()
encoder.output = [output1, output2]

# Start streaming to the network.
picam2.start_encoder(encoder)
picam2.start()
time.sleep(5)

# Start recording to a file.
output2.fileoutput = "test.h264"
output2.start()
print("Recording to file in progress.")
time.sleep(5)
output2.stop()
print("Recording stopped.")

# The file is closed, but carry on streaming to the network.
time.sleep(9999999)