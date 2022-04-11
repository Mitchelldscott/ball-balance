#! /usr/bin/env python3

import cv2
import time
import board
import busio
import numpy as np
import adafruit_pca9685

def init_servohat(freq):
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = adafruit_pca9685.PCA9685(i2c)
    pca.frequency = freq

    motorX = pca.channels[0]
    motorY = pca.channels[1]
    return pca, motorX, motorY

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

pca, motorX, motorY = init_servohat(60)
cap, w, h = init_camera()
motorY.duty_cycle = 4500

target = np.array([0.5, 0.5])
u = target

Kp = 0.25

while True:
    t = time.time()
    ret, frame = cap.read()
    if not ret:
        print("cap.read() retured False: Exiting ...")
        exit(0)

    ball, frame = detect(frame, w, h)
    capture_t = time.time() - t

    err = (target - ball) * Kp
    u = (err * 3000) + 4500 #* controller 

    print(f'ErrorX: {err[0]}, SignalX: {u[0]}')
    motorX.duty_cycle = int(u[0])

    processing_time = time.time() - capture_t - t

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
    print(f'Loop time: {np.round(time.time() - t, 4)}, {np.round(capture_t, 4)}, {np.round(processing_time, 4)}')
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()