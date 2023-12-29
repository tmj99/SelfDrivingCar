import cv2
import numpy as np
import socket
import threading

# Define the UDP server address and port
UDP_IP = "192.168.0.48"
UDP_PORT = 8000
buffersize = 1024
msgFromServer = "Connected to UDP Server"
bytesToSend = str.encode(msgFromServer)

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((UDP_IP, UDP_PORT))

# Initialize latest_frame with a blank image
latest_frame = np.zeros((480, 640, 3), dtype=np.uint8)
frame_lock = threading.Lock()  # Lock to protect access to latest_frame

def receive_udp():
    global latest_frame
    connectMsg = False
    while True:
        data, addr = udp_socket.recvfrom(buffersize)  # Receive data
        print(f"Received {len(data)} bytes from {addr}")  # Print status
        frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), -1)

        if frame is not None and frame.size > 0:
            with frame_lock:
                latest_frame = frame

        if not connectMsg:
            udp_socket.sendto(bytesToSend, addr)
            print(f'Incoming from Client at address: {addr}')
            connectMsg = True

def display_video():
    global latest_frame
    while True:
        with frame_lock:
            frame = latest_frame

        # Display the frame
        if frame is not None and frame.size > 0:
            cv2.imshow('UDP Video Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    udp_thread = threading.Thread(target=receive_udp)
    udp_thread.daemon = True
    udp_thread.start()

    display_video_thread = threading.Thread(target=display_video)
    display_video_thread.start()
