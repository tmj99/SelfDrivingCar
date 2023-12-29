import cv2
import numpy as np
import socket
import threading
import io
import av

# Define the UDP server address and port
UDP_IP = "192.168.0.48"
UDP_PORT = 8000
BufferSize = 65536
msgFromServer = "Connected to UDP Server"
bytesToSend = str.encode(msgFromServer)

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BufferSize)
udp_socket.bind((UDP_IP, UDP_PORT))

# Initialize latest_frame with a blank image
latest_frame = np.zeros((480, 640, 3), dtype=np.uint8)
frame_lock = threading.Lock()  # Lock to protect access to latest_frame

def receive_udp():
    global latest_frame
    connectMsg = False
    while True:
        data, addr = udp_socket.recvfrom(BufferSize)  # Receive data in <class 'bytes'>
        # print(f"Received {len(data)} bytes from {addr}")  # Print status
        file_like_object = io.BytesIO(data)
        try:
            container = av.open(file_like_object)
            print("Opened")
            for frame in container.decode(video=0):
                img = frame.to_image()
                frame = np.asarray(img)
                with frame_lock:
                    latest_frame = frame
                
            if not connectMsg:
                udp_socket.sendto(bytesToSend, addr)
                print(f'Incoming from Client at address: {addr}')
                connectMsg = True
        except av.AVError as e:
            print(f"Failed to decode: {e}")    

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

    display_video()
