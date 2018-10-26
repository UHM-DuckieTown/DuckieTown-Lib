from picamera import PiCamera
import time
from picamera.array import PiRGBArray
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
raw = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

#camera.capture(raw, format="bgr")
for frame in camera.capture_continuous(raw, format='bgr', use_video_port=True):
	image= raw.array

	cv2.imshow("Preview", image)
	key = cv2.waitKey(1)
	raw.truncate(0)
	if key == ord('q'):
		break
