from sklearn import svm
import time
import cv2
from skimage.feature import local_binary_pattern
import numpy as np
from joblib import load
from picamera import PiCamera
from picamera.array import PiRGBArray

global image

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

def stopSignDetect():
    if(clf.predict_proba([lbp(image)])[0][1] > 0.7):
        print('found stop sign')
    else:
        print('miss')
    #print clf.predict_proba([lbp(image)])[0][1] 

if __name__ == "__main__":
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 20
    raw = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)
    clf=load("clf_grid_Stop")
    
    for _ in camera.capture_continuous(raw, format='bgr', use_video_port=True):
        image = raw.array
        image = image[0:70, 570:640]
        stopSignDetect()
        cv2.imshow('nou', image)
        key = cv2.waitKey(1)
        raw.truncate(0)
        if key == ord('q'):
            break
