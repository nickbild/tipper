import RPi.GPIO as GPIO
import numpy as np
import cv2
import sys
import time
import videocaptureasync as vc


solenoid_pin = 23 # Pin #16
try:
    pitch_number = int(open("image_count.txt", "r").read().strip())
except:
    pitch_number = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(solenoid_pin, GPIO.OUT, initial=GPIO.LOW)

cap = vc.VideoCaptureAsync()
cap.start()

# "Warm up" the camera.
ret, img = cap.read()
time.sleep(5)

# Launch!
print("Throwing pitch...")
GPIO.output(solenoid_pin, GPIO.HIGH)

time.sleep(0.040)
ret, img1 = cap.read()
time.sleep(0.020)
ret, img2 = cap.read()

img3 = np.concatenate((img1, img2), axis=0)
cv2.imwrite("img/pitch_{}.jpg".format(pitch_number), img3)

# Save the original images in case the approach needs to change later.
cv2.imwrite("img/original/pitch_{}_1.jpg".format(pitch_number), img1)
cv2.imwrite("img/original/pitch_{}_2.jpg".format(pitch_number), img2)

GPIO.output(solenoid_pin, GPIO.LOW)
cap.stop()

pitch_number += 1
open("image_count.txt", "w").write(str(pitch_number))
