from picamera import PiCamera
import time
from picamera.array import PiRGBArray
import cv2
import paho.mqtt.publish as publish
import base64
import argparse
import numpy as np


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
raw = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

MQTT_SERVER = "192.168.0.102"
MQTT_PATH = "test_channel"


#camera.capture(raw, format="bgr")
for frame in camera.capture_continuous(raw, format='bgr', use_video_port=True):
	image= raw.array

	cv2.imshow("Preview", image)
	#img_str = cv2.imencode('.jpg', image)[1].tostring()
	#encoded_str = base64.b64encode(img_str)
	#publish.single(MQTT_PATH, encoded_str, 0,hostname = MQTT_SERVER)
        #print "Sent" + encoded_str

	key = cv2.waitKey(1)
	raw.truncate(0)
	if key == ord('q'):
		break
