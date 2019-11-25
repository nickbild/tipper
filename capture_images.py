import RPi.GPIO as GPIO
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
cap.set(3, 1280)
cap.set(4, 720)

# "Warm up" the camera.
ret, img = cap.read()
time.sleep(5)

# Launch!
print("Throwing pitch...")
GPIO.output(solenoid_pin, GPIO.HIGH)

for i in range(2):
    ret, img = cap.read()
    cv2.imwrite("img/pitch_{}_{}.jpg".format(pitch_number, i), img)

GPIO.output(solenoid_pin, GPIO.LOW)
GPIO.cleanup()

pitch_number += 1
open("image_count.txt", "w").write(str(pitch_number))

