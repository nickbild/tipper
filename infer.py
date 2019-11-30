import RPi.GPIO as GPIO
import torch
from torchvision.transforms import transforms
import numpy as np
from torch.autograd import Variable
from torchvision.models import squeezenet1_1
from PIL import Image
from train import Net
import cv2
import time
import videocaptureasync as vc


img_width = 640
img_height = 960
trained_model = "tipper_10_1.0-1.0.model"
num_classes = 2

solenoid_pin = 23 # Pin #16
green_led_pin = 25 # Pin 22.
red_led_pin = 8 # Pin 24.
GPIO.setmode(GPIO.BCM)
GPIO.setup(solenoid_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(green_led_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(red_led_pin, GPIO.OUT, initial=GPIO.LOW)


# Load the saved model.
checkpoint = torch.load(trained_model)
model = Net(num_classes=num_classes)
model.load_state_dict(checkpoint)
model.eval()

transformation = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])


def predict_image_class(image):
    # Preprocess the image.
    image_tensor = transformation(image).float()

    # Add an extra batch dimension since pytorch treats all images as batches.
    image_tensor = image_tensor.unsqueeze_(0)
    image_tensor.cuda()

    # Turn the input into a Variable.
    input = Variable(image_tensor)

    # Predict the class of the image.
    output = model(input)
    #print(output)

    index = output.data.numpy().argmax()
    score = output[0, index].item()

    return index, score


def main():
    cap = vc.VideoCaptureAsync()
    cap.start()

    # Get model resident in memory.
    img_warm_up = cv2.imread("warm_up.jpg")
    index, score = predict_image_class(img_warm_up)

    # Warm up camera.
    print("5 seconds...")
    ret, img1 = cap.read()
    time.sleep(5)

    #import datetime

    print("Throwing pitch...")
    GPIO.output(solenoid_pin, GPIO.HIGH)

    #print(datetime.datetime.now())

    time.sleep(0.140)
    ret, img1 = cap.read()
    time.sleep(0.020)
    ret, img2 = cap.read()
    img3 = np.concatenate((img1, img2), axis=0)

    #print(datetime.datetime.now())

    index, score = predict_image_class(img3)

    # Light up indicator LED.
    if index == 1:
        GPIO.output(green_led_pin, GPIO.HIGH)
    else:
        GPIO.output(red_led_pin, GPIO.HIGH)

    #print(datetime.datetime.now())

    print("Class: ", index)
    print("Score: ", score)

    cap.stop()
    GPIO.output(solenoid_pin, GPIO.LOW)
    GPIO.cleanup()


if __name__ == "__main__":
    main()

