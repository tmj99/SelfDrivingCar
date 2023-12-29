from flask import Flask, request, render_template, Response
import cv2
import numpy as np
import socket
import threading

app = Flask(__name__)

# Define the UDP server address and port
UDP_IP          = "192.168.0.48"
UDP_PORT        = 8000
buffersize      = 1024
msgFromServer   = "Connected to UDP Server"
bytesToSend = str.encode(msgFromServer)

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((UDP_IP, UDP_PORT))

# Create a global variable to store the latest video frame
latest_frame = None
frame_lock = threading.Lock()  # Lock to protect access to latest_frame

# Function to update the latest_frame variable
def update_latest_frame(frame):
    global latest_frame
    with frame_lock:
        latest_frame = frame

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Stream</title>
        <style>
            .video-container {
                width: 640px;
                height: 480px;
                border: 1px solid #000;
            }
        </style>
    </head>
    <body>
        <h1>Flask server is running</h1>
        <video id="video" class="video-container" autoplay>
            <source src="/video_feed" type="multipart/x-mixed-replace; boundary=frame">
        </video>
    </body>
    </html>
    """

def generate():
    while True:
        frame = latest_frame
        if frame is not None:
            # Encode the frame as JPEG before sending
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return app.response_class(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def receive_udp():
    global latest_frame
    connectMsg = False # initialize connection message
    while True:
        data, addr = udp_socket.recvfrom(buffersize)  # Receive data (adjust buffer size as needed)
        # Process the received UDP data as video frames
        print(f"Received {len(data)} bytes from {addr}")
        frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), -1)
        latest_frame = frame
        if not connectMsg: # send connection message and print address once when connected
            udp_socket.sendto(bytesToSend, addr)
            print(f'Incoming from Client at address: {addr}')
            connectMsg = True

if __name__ == '__main__':
    # Start a thread to receive UDP packets in the background
    udp_thread = threading.Thread(target=receive_udp)
    udp_thread.daemon = True
    udp_thread.start()

    # Start the Flask app
    app.run(host=UDP_IP, port=UDP_PORT)
