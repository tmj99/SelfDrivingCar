from flask import Flask, request
import cv2
import numpy as np
import socket
import threading

app = Flask(__name__)

# Define the UDP server address and port
UDP_IP = "192.168.0.48"  # Listen on all available network interfaces
UDP_PORT = 8000  # Port where your Raspberry Pi is sending UDP packets

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((UDP_IP, UDP_PORT))

# Create a global variable to store the latest video frame
latest_frame = None

@app.route('/')
def home():
    return "Flask server is running."

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            frame = latest_frame
            if frame is not None:
                # Encode the frame as JPEG before sending
                _, jpeg = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    return app.response_class(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def receive_udp():
    global latest_frame
    while True:
        data, addr = udp_socket.recvfrom(65535)  # Receive data (adjust buffer size as needed)
        # Process the received UDP data as video frames
        frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), -1)
        latest_frame = frame

if __name__ == '__main__':
    # Start a thread to receive UDP packets in the background
    udp_thread = threading.Thread(target=receive_udp)
    udp_thread.daemon = True
    udp_thread.start()

    # Start the Flask app
    app.run(host='0.0.0.0', port=8000)
