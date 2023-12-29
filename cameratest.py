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

output1 = FfmpegOutput("-f mpegts udp://192.168.0.48:8000")
output2 = FileOutput()
encoder.output = [output1, output2]

# Start streaming to the network.
picam2.start_encoder(encoder)
picam2.start()
time.sleep(5)

# Start recording to a file.
output2.fileoutput = "test.h264"
output2.start()
time.sleep(5)
output2.stop()

# The file is closed, but carry on streaming to the network.
time.sleep(9999999)