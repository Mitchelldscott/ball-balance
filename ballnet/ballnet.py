#! /usr/bin/env python3

import cv2
import board
import busio
import numpy as np
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 60

motorX = pca.channels[0]
motorY = pcs.channels[1]
cap = cv2.VideoCapture(0)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )

target = np.array([0.5, 0.5])

u = target

if not cap.isOpened():
    print("Cannot open camera")
    exit()

t = 0    

while True:
    t += 0.1
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # Display the resulting frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ball = np.zeros(2)

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if w * h > 40:
            ball = np.array([x / width, y / height], dtype=np.float64)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            frame = cv2.putText(frame, f'({x},{y})', (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,0,0), 2, cv2.LINE_AA)
            
    err = (target - ball) + 0.5
    u = (err * 10000) + 1000 #* controller 

    print(err, u)
    motorX.duty_cycle = int(u[0])

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()