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

def detect(img, flag):
    ss_threshold = 0.7
    tl_threshold = 0.6
    ss_hit = 0
    tl_hit = 0
    clf = load("features/clf_grid_Stop")
    #cv2.imshow('stop sign detect',img)
    neg_conf, ss_conf, tl_conf = clf.predict_proba([lbp(img)])[0]
    if(ss_conf > ss_threshold):
        #cv2.imshow('stop sign detect',img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        flag.put(1)
        ss_hit = 1
    if(tl_conf > tl_threshold):
        #cv2.imshow('traffic light detect',img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        tl_hit = 1
    print '({} {} {})'.format(neg_conf, ss_conf, tl_conf)
    return (ss_hit, tl_hit)

