#!/usr/bin/python3

"""
S T R E A M I N G
This section enables the visual of the car to be streamed at
https:// <ip of the pi> :8000/stream.mjpg
"""

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import io
import logging
import socketserver
from http import server
from threading import Condition, Thread

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

PAGE = """\
<html>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<h1>Picamera2 MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

"""
C O N T R O L S
This section is mainly for the controls of the car
Will try to get the webstream to be able to get controls of the car
"""

from Motor import *
import pygame

pygame.init()
screen = pygame.display.set_mode((100,100))

PWM = Motor()

def start_session():

    try:
        while True:
            # print("Speed of:",speeds)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        PWM.setMotorModel(1000,1000,1000,1000)
                        print("Forward ...")
                    elif event.key == pygame.K_s:
                        PWM.setMotorModel(-1000,-1000,-1000,-1000)
                        print("Backward ...")
                    elif event.key == pygame.K_a:
                        PWM.setMotorModel(-1000,-1000,2000,2000)
                        print("Rotating left ... ")
                    elif event.key == pygame.K_d:
                        PWM.setMotorModel(2000,2000,-1000,-1000)
                        print("Rotating right ... ")
                    elif event.key == pygame.K_SPACE:
                        PWM.setMotorModel(0,0,0,0)
                        print("Stopping ...")

    except KeyboardInterrupt:
        PWM.setMotorModel(0,0,0,0)
        print ("\nEnd of program")
        return

if __name__ == '__main__':
    # ... (Rest of the code for streaming setup)

    car_control_thread = Thread(target=start_session)

    # Start the car control thread
    car_control_thread.start()

    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        picam2.stop_recording()