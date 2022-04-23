#! /usr/bin/env python3

import sys
import cv2
import time
import board
import busio
import numpy as np
import adafruit_pca9685


def init_servohat(freq):
	i2c = busio.I2C(board.SCL, board.SDA)
	pca = adafruit_pca9685.PCA9685(i2c)
	pca.frequency = 60

	motorX = pca.channels[0]
	motorY = pca.channels[1]
	return pca, motorX, motorY

def spin(step):
	pca, motorX, motorY = init_servohat(60)

	high = 3000 / 2

	low = 3000

	t = 0

	while 1:
		signal = (high * (np.cos(t) + 1)) + low
		print(signal)
		motorX.duty_cycle = int(signal)
		motorY.duty_cycle = int(signal)
		t += step
		time.sleep(0.1)

def set(value):
	pca, motorX, motorY = init_servohat(60)

	motorX.duty_cycle = int(value)
	motorY.duty_cycle = int(value)


def main(args):
	if len(args) < 2:
		spin(1 / (10 * np.pi))

	if len(args) == 2:
		set(args[1])

if __name__ == '__main__':
	main(sys.argv)