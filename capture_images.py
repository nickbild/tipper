import RPi.GPIO as GPIO
import numpy as np
import cv2
import sys
import time


solenoid_pin = 23 # Pin #16
try:
    pitch_number = int(open("image_count.txt", "r").read().strip())
except:
    pitch_number = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(solenoid_pin, GPIO.OUT, initial=GPIO.LOW)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, 0x47504A4D) # MJPG codec.
cap.set(3, 640)
cap.set(4, 480)

# "Warm up" the camera.
ret, img = cap.read()
time.sleep(5)

# Launch!
print("Throwing pitch...")
GPIO.output(solenoid_pin, GPIO.HIGH)

time.sleep(0.220)
ret, img1 = cap.read()
time.sleep(0.005)
ret, img2 = cap.read()

img = np.concatenate((img1, img2), axis=0)
cv2.imwrite("img/pitch_{}.jpg".format(pitch_number), img)

# Save the original images in case the approach needs to change later.
cv2.imwrite("img/original/pitch_{}_1.jpg".format(pitch_number), img1)
cv2.imwrite("img/original/pitch_{}_2.jpg".format(pitch_number), img2)

GPIO.output(solenoid_pin, GPIO.LOW)

pitch_number += 1
open("image_count.txt", "w").write(str(pitch_number))

