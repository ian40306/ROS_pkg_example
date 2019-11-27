import cv2
import picamera
import numpy as np
import time
import socket
i=0
with picamera.PiCamera() as camera:
	camera.resolution = (640, 480)
	camera.framerate = 24
	time.sleep(1)
	print("before socket")
	### Connect to GPU computer ###
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("192.168.66.248", 5050))
	print("after socket")

	### Take a picture ###
	image = np.empty((480 * 640 *3,), dtype=np.uint8)
	camera.capture(image, format='bgr')
	image = image.reshape((480, 640, 3))
	cv2.imwrite("/home/titi/duckietown/123.jpg", image)
	### Create socket with GPU computer ###
	### Send image to GPU computer ###
	imgFile = open("/home/titi/duckietown/123.jpg")
	while True:
		imgData = imgFile.readline(1024)
		if not imgData:
			s.send("over")
			break
		s.send(imgData)
	imgFile.close()
	print("transit end")
	while True:
		global i
		location = s.recv(1024)
		if location == "over":
			print(location)
			break
		else:
			if i==6:
				print("*********  next  **********")
				i=0
			print(location)
				i+=1
	print("socket deconnection...")
	s.close()
