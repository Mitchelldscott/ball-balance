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
import multiprocessing
import adafruit_pca9685

from pid import PID
from cv_detector import CV2_Detector
from servo_driver import Adafruit_Servo_Driver

def Detector_thread(config_data, measurement):
	detector = CV2_Detector(config_data)
	detector.spin(measurement)

def PID_thread(config_data, measurement):
	controller = PID(config_data)
	controller.spin(measurement)

def Driver_thread(config_data, measurement):
	servo_driver = Adafruit_Servo_Driver(config_data)
	time.sleep(5)
	servo_driver.spin(measurement)

def main(config_data):

	stateX = multiprocessing.Array('f', 2)
	stateY = multiprocessing.Array('f', 2)
	controlX = multiprocessing.Value('f', 0.0)
	controlY = multiprocessing.Value('f', 0.0)


	p1 = multiprocessing.Process(target=Detector_thread, args=(config_data['CAMERA'], (stateX, stateY)))
	p2 = multiprocessing.Process(target=Driver_thread, args=(config_data['SERVO_DRIVER_X'], controlX))
	p3 = multiprocessing.Process(target=Driver_thread, args=(config_data['SERVO_DRIVER_Y'], controlY))
	p2 = multiprocessing.Process(target=PID_thread, args=(config_data['PID_X'], (stateX, controlX)))
	p3 = multiprocessing.Process(target=PID_thread, args=(config_data['PID_Y'], (stateY, controlY)))

	p1.start()
	p2.start()	
	p3.start()

	running = True

	try:
		while running:
			if not p1.is_alive():
				p2.terminate()
				p3.terminate()
				print(f'Detector Finished')
				running = False
			if not p2.is_alive():
				p1.terminate()
				p3.terminate()
				print(f'Driver Finished')
				running = False

	except KeyboardInterrupt as e:
		print(e)
		print(f'Terminating Run')
		p1.terminate()
		p2.terminate()
		p3.terminate()


if __name__ == '__main__':

	config_path = os.path.join(os.getenv('PROJECT_ROOT'), 'ballpy', 'config', 'data')

	if len(sys.argv) == 2:
		file = sys.argv[1]
	else:
		file = 'default.yaml'

	with open(os.path.join(config_path, file), 'r') as f:
		data = yaml.safe_load(f)
	
	main(data)













