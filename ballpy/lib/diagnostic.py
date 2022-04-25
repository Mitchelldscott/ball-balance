#! /usr/bin/env python3

import os
import sys
import time
import yaml
import numpy as np
import matplotlib.pyplot as plt

def readFile(file):
	with open(file, 'r') as f:
		text = f.readlines()

	data = []
	for line in text:
		items = line.split(',')
		data.append([float(value) for value in items])

	return data

def plot_path(ax, x, y, color, marker, vx=None, vy=None):
	ax.plot(x, y, color=color, marker=marker)

	if not vx is None and not vy is None:
		for (x, y, vx, vy) in zip(x,y,vx,vy):
			ax.arrow(x, y, vx*10, vy*10, color=color)

	return ax

def plot_time(ax, ux, uy, t, colors=['b', 'r']):
	ax.plot(t, ux, color=colors[0])
	ax.plot(t, uy, color=colors[1])
	return ax

def analyze(det_data, driver_data, file):
	fig, axes = plt.subplots(2,2, figsize=(12,6))
	axes[0][0].set_xlim(0, 600)
	axes[0][0].set_ylim(0, 480)


	td, xd, yd, wd, hd = zip(*det_data)
	td = np.array(td) - td[0]
	axes[0][0] = plot_path(axes[0][0], 600-np.array(xd), yd, 'b', '>')

	tr, tm, xr, yr, vx, vy, ux, uy = zip(*driver_data)

	tr = np.array(tr) - tr[0] + 5
	xr = (-np.array(xr) + 1) * 300
	yr = (np.array(yr) + 1) * 240
	axes[0][0] = plot_path(axes[0][0], xr, yr, 'r', 'x', vx=vx, vy=vy)
	axes[0][1] = plot_time(axes[0][1], ux, uy, tr)

	axes[1][0] = plot_time(axes[1][0], 600-np.array(xd), yd, td)
	axes[1][0] = plot_time(axes[1][0], xr, yr, tr, colors=['c', 'm'])

	plt.savefig(file)
	plt.show()


def main():
	data_path = os.path.join(os.getenv('PROJECT_ROOT'), 'ballpy', 'data')
	detector_data = readFile(os.path.join(data_path, 'ballnet-log.txt'))
	driver_data = readFile(os.path.join(data_path, 'driver-log.txt'))
	save_file = os.path.join(data_path, 'diagnostic.jpg')

	analyze(detector_data, driver_data, save_file)

if __name__ == '__main__':
	main()