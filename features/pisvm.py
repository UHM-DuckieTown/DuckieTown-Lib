from sklearn import svm
import time
import cv2
from skimage.feature import local_binary_pattern
import numpy as np
from joblib import load
from picamera import PiCamera
from picamera.array import PiRGBArray
from contours import find_red
import os
from random import randint

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
    ss_threshold = 0.55
    tl_threshold = 0.5
    ss_hit = 0
    tl_hit = 0
    #flag.value = 0
    if flag.value == 0:
        clf = load("features/clf_grid_Stop")
        neg_conf, ss_conf, tl_conf = clf.predict_proba([lbp(img)])[0]
        if(ss_conf > ss_threshold):
            '''
            img_name = "a28"+str(randint(0,1000))+".png"
            cv2.imshow("stop sign??", img)
            k = cv2.waitKey(5000)
            if k%256 == 27:  # ESC for positives
                path = os.path.join("/features/dataset/ss_positives",img_name)
                cv2.imwrite(path, img)
                print "saved stop sign positive image to {}".format(path)
            elif k%256 == 32:   # SPACE for negatives
                path = os.path.join("/features/dataset/negatives",img_name)
                cv2.imwrite(path, img)
                print "saved negative image to {}".format(path)
            '''
            flag.value = 1
            ss_hit = 1
        elif(tl_conf > tl_threshold):
            if len(find_red(img, 30, 350,slider, twofeed)) == 1:
                # requires contour area to be min 30px^2 and max 350px^2 to be an LED
                flag.value = 1
                tl_hit = 1
        else:
            flag.value = 0
        #print '({} {} {})'.format(neg_conf, ss_conf, tl_conf)
        #if flag.value == 1:
        #cv2.imshow("stop", img)
        #cv2.waitKey(1)
    return (ss_hit, tl_hit)
