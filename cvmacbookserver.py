import cv2
import numpy as np
import socket
import threading

# Define the UDP server address and port
UDP_IP          = "192.168.0.48"
UDP_PORT        = 8000
buffersize      = 1024
msgFromServer   = "Connected to UDP Server"
bytesToSend     = str.encode(msgFromServer)

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((UDP_IP, UDP_PORT))

# Create a global variable to store the latest video frame
latest_frame = None
frame_lock = threading.Lock()  # Lock to protect access to latest_frame

def receive_udp():
    global latest_frame
    connectMsg = False
    while True:
        data, addr = udp_socket.recvfrom(buffersize)  # Receive data
        frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), -1)

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

        if frame is not None:
            # Display the frame
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
