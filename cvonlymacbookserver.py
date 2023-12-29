#!/usr/bin/python3

import cv2, socket
import numpy as np
import time
import base64

# UDP Client-Server interaction
host_ip        = "192.168.0.48"
port           = 8000
BUFF_SIZE      = 65536

server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

fps,st,frames_to_count,cnt = (0,0,20,0)

msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
print('GOT connection from ',client_addr)
print(msg)
message = b'You are connected'
server_socket.sendto(message,client_addr)

while True:	
	packet,_ = server_socket.recvfrom(BUFF_SIZE)
	print(f'Length of packet: {len(packet)}')
	try:
		data = base64.b64decode(packet,' /')
		print(f'Length of data: {len(data)}')
		npdata = np.fromstring(data,dtype=np.uint8)
		frame = cv2.imdecode(npdata,1)
		frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
		cv2.imshow("RECEIVING VIDEO",frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			server_socket.close()
			break
		if cnt == frames_to_count:
			try:
				fps = round(frames_to_count/(time.time()-st))
				st=time.time()
				cnt=0
			except:
				pass
		cnt+=1
	except:
		print("Something went wrong")