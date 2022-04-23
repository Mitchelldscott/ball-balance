#! /usr/bin/env python3

#
#	Imports
#

import os
import sys
import cv2
import time
import yaml
import board
import busio
import numpy as np
import adafruit_pca9685



#
#	OpenCV Ball detector
#

class CV2_Detector():
	def __init__(self, config_data):

		self.lives = 10

		self.camera = cv2.VideoCapture(0)

		if ('FPS' in config_data):
			self.camera.set(cv2.CAP_PROP_FPS, config_data['FPS'])

		if 'DEBUG' in config_data:
			self.debug = config_data['DEBUG']
		else:
			self.debug = False
		
		width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
		self.shape = np.array([height, width, 3])

		if 'CROP' in config_data:
			self.crop = np.array(config_data['CROP'])
		else:
			self.crop = np.array([[0, height], [0, width]])

		if not self.camera.isOpened():
			print("Cannot open camera")
			exit()

	def damage(self):
		if self.live > 0:
			self.lives -= 1
		else:
			print('\n\tOut of lives: Exiting ...')
			exit

	def detect(self):
		ret, frame = self.camera.read()
		
		if not ret:
			self.damage()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
		contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		ball = np.zeros(2)

		for cnt in contours:
			x,y,w,h = cv2.boundingRect(cnt)
			if w * h > 100 and np.abs((w / h) - 1) <  0.25:
				ball = np.array([x / self.shape[1], y / self.shape[0]], dtype=np.float64)
				cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
				frame = cv2.putText(frame, f'({x},{y})', (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
				break

		return ball, frame

	def spin(self):

		try: 
			while True:
				t = time.time()
				ball, image = self.detect()
				capture_t = time.time() - t

				if self.debug:
					cv2.imshow('frame', image)
					if cv2.waitKey(1) == ord('q'):
						break

					if self.debug == 2:
						print(f'Capture time: {capture_t}')

		except KeyboardInterrupt as e:
			self.cleanup()
			print(e)
			print('Terminate Recieved: Exiting...')

	def cleanup(self):
		self.camera.release()
		cv2.destroyAllWindows()

#
#	Adafruit Servo Driver UX
#

class Adafruit_Servo_Driver():
	def __init__(self, config_data):
		i2c = busio.I2C(board.SCL, board.SDA)
		pca = adafruit_pca9685.PCA9685(i2c)
		pca.frequency = freq

		motorX = pca.channels[0]
		motorY = pca.channels[8]
		return pca, motorX, motorY
	


def main(config_data):

	detector = CV2_Detector(config_data['CAMERA'])
	detector.spin()
	# motorY.duty_cycle = 4500

	# target = np.array([0.5, 0.5])
	# u = target

	# Kp = 0.25

	# while True:
	# 	t = time.time()
	# 	ret, frame = cap.read()
	# 	if not ret:
	# 		print("cap.read() retured False: Exiting ...")
	# 		exit(0)

	# 	ball, frame = detect(frame, w, h)
	# 	capture_t = time.time() - t

	# 	err = (target - ball) * Kp
	# 	u = (err * 3000) + 4500 #* controller 

	# 	print(f'ErrorX: {err[0]}, SignalX: {u[0]}')
	# 	motorX.duty_cycle = int(u[0])

	# 	processing_time = time.time() - capture_t - t

	# 	cv2.imshow('frame', frame)
	# 	if cv2.waitKey(1) == ord('q'):
	# 		break
	# 	print(f'Loop time: {np.round(time.time() - t, 4)}, {np.round(capture_t, 4)}, {np.round(processing_time, 4)}')
			
	# # When everything done, release the capture
	# cap.release()
	# cv2.destroyAllWindows()




if __name__ == '__main__':

	config_path = os.path.join(os.getenv('PROJECT_ROOT'), 'ballpy', 'config', 'data')

	if len(sys.argv) == 2:
		file = sys.argv[1]
	else:
		file = 'default.yaml'

	with open(os.path.join(config_path, file), 'r') as f:
		data = yaml.safe_load(f)
	
	main(data)













