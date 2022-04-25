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


class PID:
	"""
		A generic PID controller object.
		SISO, expects normalized input
	"""
	def __init__(self, data):
		"""
			da setup
		"""
		self.debug = data['DEBUG']
		# K is a list [kp, ki, kd]
		data['K'] = np.array(data['K'])

		self.t = time.time()
		self.measure_t = self.t

		self.x = None
		self.ix = None
		self.dx = None

		self.U = 0.0

		self.data = data

	def filter(self):
		t = time.time()
		dt = (t - self.t)
		self.t = t

		if not self.dx is None:
			if not self.x is None:
				self.x += self.dx * dt
				if self.ix is None:
					self.ix = self.x * dt
				else:
					self.ix += self.x * dt

			else:
				self.x = self.dx * dt

		self.dx += 7 * self.U * dt
		
		if not self.ix is None:
			self.U += (-self.data['K'] @ np.array([[self.x], [self.ix], [self.dx]]))[0]


	def spin(self, measurement):

		if measurement is not None:
			self.x = measurement[0]
			self.dx = measurement[1]
		else:
			[self.x, self.dx] = [1.0, 0.0]

		while True:

			if self.debug:
				print(f'State:\n\t[{self.x}, {self.ix}, {self.dx}]')
				print(f'U:\n\t{self.U}')

				if self.debug == 3:
					info = np.array([self.t,  self.x, self.ix, self.dx, self.U])
					s = ','.join(format(x, "10.4f") for x in info)
					file = os.path.join(os.getenv('PROJECT_ROOT'), 'ballpy', 'data', f'PID-{os.getpid()}.txt')
					with open(file , 'a+') as f:
						f.write(s + '\n')

			self.filter()
			
			if measurement is not None:
				self.x = measurement[0]
				self.dx = measurement[1]
			else:
				[self.x, self.dx] = [1.0, 0.0]


def main(file):
	config_path = os.path.join(os.getenv('PROJECT_ROOT'), 'ballpy', 'config', 'data')

	if file[-5] == '.yaml':
		config_file = os.path.join(config_path, file)
	else:
		config_file = os.path.join(config_path, file + '.yaml')

	with open(config_file, 'r') as f:
		data = yaml.safe_load(f)

	controller = PID(data['PID'])

	controller.spin([0,0])


if __name__ == '__main__':
	if len(sys.argv) > 1:
		main(sys.argv[1])

	else:
		main('default')