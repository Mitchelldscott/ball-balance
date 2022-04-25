#! /usr/bin/env python3

#
#	Imports
#

import os
import sys
import cv2
import time
import yaml
import numpy as np


#
#	OpenCV Ball detector
#

class CV2_Detector():
	def __init__(self, data):

		self.lives = 10

		self.t = time.time()

		self.debug = data['DEBUG']

		self.camera = cv2.VideoCapture(0)
		self.camera.set(cv2.CAP_PROP_FPS, data['FPS'])
		self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, data['SHAPE'][1])
		self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, data['SHAPE'][0])

		data['SHAPE'] = np.array(data['SHAPE'])
		data['CROP'] = (data['SHAPE'].reshape((2,1)) * np.array(data['CROP'])).astype(int)
		data['ADJ_SHAPE'] = data['CROP'][:,1] - data['CROP'][:,0]

		self.data = data

		if not self.camera.isOpened():
			print("Cannot open camera")
			exit()

	def damage(self):
		if self.live > 0:
			self.lives -= 1
		else:
			print('\n\tOut of lives: Exiting ...')
			exit

	def crop(self, image):
		return image[self.data['CROP'][0,0]:self.data['CROP'][0,1], 
					 self.data['CROP'][1,0]:self.data['CROP'][1,1]]

	def detect(self):
		
		self.t = time.time()

		ret, frame = self.camera.read()
		cropped = self.crop(frame)
		display = cropped.copy()

		if not ret:
			self.damage()

		gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
		ret, thresh = cv2.threshold(gray, self.data['THRESHOLD'], 255, cv2.THRESH_BINARY_INV)
		contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		pose = None
		info = None

		for i,cnt in enumerate(contours):
			x,y,w,h = cv2.boundingRect(cnt)

			a = w * h
			xc = x + round(w / 2, 0)
			yc = y + round(h / 2, 0)

			if a > self.data['BALL_AREA'][0] and  a < self.data['BALL_AREA'][1] and np.abs((w / h) - 1) <  1e-1:
				
				pose = np.array([2 * xc / cropped.shape[1],
								 2 * yc / cropped.shape[0]], dtype=np.float64) - 1

				info = [self.t, xc, yc, w, h]

				if self.debug > 1:
					mask = cv2.bitwise_and(gray, thresh)
					shape = (mask.shape[0], mask.shape[1], 1)
					mask = np.concatenate([mask.reshape(shape), mask.reshape(shape), mask.reshape(shape)], axis=2)
					cv2.rectangle(cropped, (x,y), (x+w,y+h), (0,255,0), 2)
					cropped = cv2.putText(cropped, f'({xc},{yc})', (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 
										 1, (10,10,10), 2, cv2.LINE_AA)
					display = np.concatenate([display, mask, cropped], axis=1)
				
				break

		return pose, display, info

	def spin(self, measurement):

		try: 
			while True:
				ball, image, info = self.detect()

				if not ball is None:
					measurement[0] = ball[0]
					measurement[1] = ball[1]
					measurement[2] = time.time()
				else:
					measurement[2] = -1

				if self.debug:
					print(f'Detection: {measurement[2]}\n\t{ball}')

					if self.debug == 3 and not info is None:
						s = ','.join(format(x, "10.4f") for x in info)
						file = os.path.join(os.getenv('PROJECT_ROOT'), 'ballpy', 'data', 'ballnet-log.txt')
						with open(file , 'a+') as f:
							f.write(s + '\n')

					elif self.debug == 2:
						cv2.imshow('frame', image)
						if cv2.waitKey(1) == ord('q'):
							break

		except KeyboardInterrupt as e:
			self.cleanup()
			print(e)
			print('Terminate Recieved: Exiting...')

	def cleanup(self):
		self.camera.release()
		cv2.destroyAllWindows()


def main(file):
	config_path = os.path.join(os.getenv('PROJECT_ROOT'), 'ballpy', 'config', 'data')

	if file[-5] == '.yaml':
		config_file = os.path.join(config_path, file + '.yaml')
	else:
		config_file = os.path.join(config_path, file + '.yaml')

	with open(config_file, 'r') as f:
		data = yaml.safe_load(f)

	detector = CV2_Detector(data['CAMERA'])

	detector.spin(np.array([1.0, 1.0, 0.0]))


if __name__ == '__main__':
	if len(sys.argv) > 1:
		main(sys.argv[1])

	else:
		main('default')









