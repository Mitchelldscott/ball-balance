#! /usr/bin/env python3

import cv2
import time
import board
import busio
import numpy as np
import adafruit_pca9685

def init_camera():

	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FPS, 30)
	# cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
	# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
	width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

	if not cap.isOpened():
		print("Cannot open camera")
		exit()

	return cap, width, height

def detect(image, width, height):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	ball = np.zeros(2)

	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		if w * h > 100 and np.abs((w / h) - 1) <  0.25:
			ball = np.array([x / width, y / height], dtype=np.float64)
			cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
			image = cv2.putText(image, f'({x},{y})', (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
			break

	return ball, image

def main():
	cap, w, h = init_camera()
	while True:
		ret, frame = cap.read()
		if not ret:
			print("cap.read() retured False: Exiting ...")
			exit(0)

		ball, frame = detect(frame, w, h)
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) == ord('q'):
			break



if __name__ == '__main__':
	main()
