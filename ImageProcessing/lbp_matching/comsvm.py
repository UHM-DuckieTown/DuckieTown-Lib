from sklearn import svm
import time
import cv2
from skimage.feature import local_binary_pattern
import numpy as np
import joblib
#from picamera import PiCamera
#from picamera.array import PiRGBArray
def lbp(test_image):

    #convert to grayscale image
    im_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    #set pts & radius
    radius = 1
    no_points = 8
    lbp = local_binary_pattern(im_gray, no_points, radius, method='uniform')
    x = lbp.ravel()
    hist, _ = np.histogram(x,bins = (no_points+2), range =(0,no_points+2), density = True)
    #add values to set
    return hist

#camera = PiCamera()
camera = cv2.VideoCapture(0)
#camera.resize = (640, 480)
#camera.framerate = 20
#raw = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
clf=joblib.load("clf_grid_Stop")
#camera.capture(raw, format="bgr")
#for frame in camera.capture_continuous(raw, format='bgr', use_video_port=True):
while True:
    ret, image = camera.read()
    #image= raw.array
    image= image[0:70,570:640]
    if(clf.predict([lbp(image)])==1):
        print('stop')
    key = cv2.waitKey(1)
#raw.truncate(0)
    cv2.imshow("nou", image)
    if key == ord('q'):
        break

