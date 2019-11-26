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


img_width = 640
img_height = 960
trained_model = "homer_0_2-1.model"
num_classes = 2

solenoid_pin = 23 # Pin #16
GPIO.setmode(GPIO.BCM)
GPIO.setup(solenoid_pin, GPIO.OUT, initial=GPIO.LOW)


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
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    # Warm up camera.
    print("5 seconds...")
    ret, img1 = cap.read()
    time.sleep(5)

    if cap.isOpened():
        print("Throwing pitch...")
        GPIO.output(solenoid_pin, GPIO.HIGH)

        ret, img1 = cap.read()
        ret, img2 = cap.read()
        img = np.concatenate((img1, img2), axis=0)
        #cv2.imwrite("img/pitch_{}.jpg".format(pitch_number), img)

        index, score = predict_image_class(img)

        print("Class: ", index)
        print("Score: ", score)

        # TODO: Light LED based on class/score for several seconds.  R unless sufficient strike score.

        cap.release()
        GPIO.output(solenoid_pin, GPIO.LOW)
        GPIO.cleanup()
    else:
        print('Unable to open camera.')


if __name__ == "__main__":
    main()