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
#	Adafruit Servo Driver UX
#

class Adafruit_Servo_Driver():
	"""
		The adafruit servo driver is a controller interface
		to a servo driver. The compatible drivers are the PCA9685
		and the Adeept 16 channel servo hat.
	
	"""
	def __init__(self, data):
		"""
			Initialize the bus, pca and
			motors.
			PARAMS:
				data: dictionary, configuration data
		"""
		i2c = busio.I2C(board.SCL, board.SDA)
		self.pca = adafruit_pca9685.PCA9685(i2c)

		self.debug = data['DEBUG']
		self.pca.frequency = data['Hz']

		m = data['CHANNEL']
		self.motor = self.pca.channels[m]
		self.t = time.time()
		self.R = 0.0

		self.data = data

		self.update_IO()

	def boundR(self):
		"""
			Make sure the reference is between the
			actuators limits.
		"""
		if self.R > self.data['RLIM']:
			self.R = self.data['RLIM']
		elif self.R < -self.data['RLIM']:
			self.R = -self.data['RLIM']

	def update_IO(self):
		"""
			Update the motor with a P controlled signal.
		"""
		self.boundR()
		
		u = (self.R * self.data['SCALE']) + self.data['OFFSET'] - self.motor.duty_cycle

		self.motor.duty_cycle += int(self.data['K'] * u)

		return time.time()

	def spin(self, R=None):
		if R is None:
			self.R = np.cos(self.t)
		else:
			self.R = R.value

		self.R *= self.data['RLIM']

		while True:
			
			if self.debug:
				print(f"Reference ({self.data['CHANNEL']}):\n\t{self.R}")
				print(f"Duty Cycle ({self.data['CHANNEL']}):\n\t{self.motor.duty_cycle}")

				if self.debug > 1:
					file = os.path.join(os.getenv('PROJECT_ROOT'), 'ballpy', 'data', 'driver-log.txt')
					info = np.array([self.t, self.R, self.motor.duty_cycle])
					s = ','.join(format(x, "10.4f") for x in info)
					with open(file , 'a+') as f:
						f.write(s + '\n')

			t = self.update_IO()

			if (t - self.t) < self.data['CYCLE_TIME']:
				sleep = max(self.data['CYCLE_TIME'] - (time.time() - self.t), 0)
				time.sleep(sleep)
			
			self.t = t

			if not R is None:
				if R != self.R:
					self.R = R.value
			else:
				self.R = np.cos(self.t)

			self.R *= self.data['RLIM']



def main(file):
	config_path = os.path.join(os.getenv('PROJECT_ROOT'), 'ballpy', 'config', 'data')

	if file[-5] == '.yaml':
		config_file = os.path.join(config_path, file)
	else:
		config_file = os.path.join(config_path, file + '.yaml')

	with open(config_file, 'r') as f:
		data = yaml.safe_load(f)

	driver = Adafruit_Servo_Driver(data['SERVO_DRIVER_X'])

	driver.spin()


if __name__ == '__main__':
	if len(sys.argv) > 1:
		main(sys.argv[1])

	else:
		main('default')
