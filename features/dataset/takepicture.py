import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import sys

filename = sys.argv[1]
img_counter = int(sys.argv[2])

camera = PiCamera()
camera.resolution = (640,480)
raw = PiRGBArray(camera, size=(640, 480))

for frame in camera.capture_continuous(raw, format='bgr', use_video_port=True):
    image = raw.array
    image = image[140:310, 420:490, :]

    cv2.imshow("test", image)
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "{}_{}.png".format(filename, img_counter)
        cv2.imwrite(img_name, image)
        print("{} written!".format(img_name))
        img_counter += 1
    raw.truncate(0)

cam.release()

cv2.destroyAllWindows()
