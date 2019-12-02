# Tipper

Tipper predicts if a pitch will be in or out of the strike zone in real time.  The batter will see a green or red light illuminate in their peripheral vision if the pitch will be in or out of the strike zone, respectively.

<p align="center">
<img src="https://raw.githubusercontent.com/nickbild/tipper/master/media/video.gif">
</p>

Higher resolution video in [Media](https://github.com/nickbild/tipper#media) section below.

## How It Works

A modified Nerf tennis ball launcher is programmatically fired with a solenoid.  A 100FPS camera is pointed in the direction of the launcher and captures two successive images of the ball early in flight.

A convolutional neural network running on an NVIDIA Jetson AGX Xavier rapidly classifies these images against a model that was built during the training phase of the project.  If the images are classified as in the strike zone, a green LED on a pair of glasses (in the wearer's peripheral vision) is lit.  Conversely, if the ball is predicted to be out of the strike zone, a red LED is lit.

## Media

See it in action: [YouTube](https://www.youtube.com/watch?v=dkE9XCBSyhw)

The ball launcher.  The rubber bands remove some of the force required to pull the trigger, giving the solenoid an assist.  The trigger return spring was also removed for the same reason.
![launcher](https://raw.githubusercontent.com/nickbild/tipper/master/media/launcher_sm.jpg)

Looking down the barrel:
![launcher barrel](https://raw.githubusercontent.com/nickbild/tipper/master/media/launcher_barrel_sm.jpg)

The processing:
![launcher](https://raw.githubusercontent.com/nickbild/tipper/master/media/xavier_sm.jpg)

Camera:
![launcher](https://raw.githubusercontent.com/nickbild/tipper/master/media/camera_sm.jpg)

The glasses:
![launcher](https://raw.githubusercontent.com/nickbild/tipper/master/media/glasses_sm.jpg)

## Software

### Training

[A CNN was built](https://github.com/nickbild/tipper/blob/master/train.py) using PyTorch.  The model was kept as small as possible as inference times on the order of tens of milliseconds are required.

Collection of training data was automated with [capture_images.py](https://github.com/nickbild/tipper/blob/master/capture_images.py).

Data should be structured as:

```
data/
    test/
        ball/
        strike/
    train/
        ball/
        strike/
```

Training can then be started with the command:

```
python3 train.py
```

### Inference

The [inference script](https://github.com/nickbild/tipper/blob/master/infer.py) pitches a ball and captures images of it in flight.  The image is classified against the CNN model, and based on the result, a green or red LED is lit on a pair of glasses worn by the batter.

To run it, cock and load the ball launcher.  Then run:

```
python3 infer.py
```

## Bill of Materials

- NVIDIA Jetson AGX Xavier
- USB camera with minimum 100FPS @ 640x480
- 3V-5V logic level shifter
- Red and green LEDs
- Power MOSFET
- 45 Newton or greater solenoid
- Nerf dog tennis ball launcher
- 2 x Breadboard
- Glasses / sunglasses
- Miscellaneous copper wire
- Plywood, miscellaneous wood screws, wooden dowels, rubber bands, hot glue

## Future Direction

## About the Author

[Nick A. Bild, MS](https://nickbild79.firebaseapp.com/#!/)
