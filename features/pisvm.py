from sklearn import svm
import time
import cv2
from skimage.feature import local_binary_pattern
import numpy as np
from joblib import load
from picamera import PiCamera
from picamera.array import PiRGBArray

def lbp(test_image):
    #convert to grayscale image
    im_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    #set pts & radius
    radius = 1
    no_points = 8
    #circular lbp
    lbp = local_binary_pattern(im_gray, no_points, radius, method='uniform')
    x = lbp.ravel()
    hist, _ = np.histogram(x,bins = (no_points+2), range =(0,no_points+2), density = True)
    #add values to set
    return hist

def stopSignDetect(img, flag):
    clf = load("features/clf_grid_Stop")
    #cv2.imshow('stop sign detect',img)
    if(clf.predict_proba([lbp(img)])[0][1] > 0.7):
        print('found stop sign')
        # cv2.imshow('stop sign detect',img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        flag.put(1)
        return 1
    else:
        print('miss')
        flag.put(0)
        return 0
