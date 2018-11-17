from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import time
import paho.mqtt.publish as publish
import base64
import numpy as np

MQTT_SERVER = "168.105.252.131"
MQTT_PATH = "test_channel"

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
raw = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

for frame in camera.capture_continuous(raw, format='bgr', use_video_port=True):
	image= raw.array
	
        publish.single(MQTT_PATH, test, hostname=MQTT_SERVER)
