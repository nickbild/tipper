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
cap.set(3, 640)
cap.set(4, 480)

# "Warm up" the camera.
ret, img = cap.read()
time.sleep(5)

# Launch!
print("Throwing pitch...")
GPIO.output(solenoid_pin, GPIO.HIGH)

ret, img1 = cap.read()
ret, img2 = cap.read()
img = np.concatenate((img1, img2), axis=0)
cv2.imwrite("img/pitch_{}.jpg".format(pitch_number), img)

GPIO.output(solenoid_pin, GPIO.LOW)
GPIO.cleanup()

pitch_number += 1
open("image_count.txt", "w").write(str(pitch_number))
