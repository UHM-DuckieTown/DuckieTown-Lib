from __future__ import division
import numpy as np
import cv2
from PIL import Image
import sys
from sklearn import svm
import time
from skimage.feature import local_binary_pattern
from joblib import load
import os
from matplotlib import pyplot as plt
from math import cos, sin
import imutils
from random import randint
from imutils.video import FPS

from pi_video_stream import PiCamVideoStream

def sliding_window(image, stepSize, windowSize):
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            cv2.imwrite("sliding_window{}-{}.png".format(x,y),image[y:y + windowSize[1], x:x + windowSize[0]])
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

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

def detect(img):
    ss_threshold = 0.35
    tl_threshold = 0.5
    ss_hit = 0
    tl_hit = 0
    clf = load("clf_grid_Stop")
    neg_conf, ss_conf, tl_conf = clf.predict_proba([lbp(img)])[0]
    if(ss_conf > ss_threshold):
        ss_hit = 1
    return ss_hit

def find_red(image, min, max):
    '''
    min: minimum contour area
    max: maximum contour area
    min/max area are the allowed range for the desired contour being represented -> used to find stop sign and red LED
    '''
    offset = 20
    image_blur = cv2.medianBlur(image, 23)
    cv2.imwrite('medianBlur.png', image_blur)
    #hsv - sepparates color from brightness
    image_blur_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #lower mask (0-10)
    lower = np.array([0,50,50])
    upper = np.array([10,255,255])
    mask0 = cv2.inRange(image_blur_hsv, lower, upper)

    #upper mask (170-180)
    lower = np.array([170,50,50])
    upper = np.array([180,255,255])
    mask1 = cv2.inRange(image_blur_hsv, lower, upper)


    #join mask
    mask = mask0+mask1
    cv2.imwrite('hsv.png', mask)

    #cv2.imshow("red mask", mask)
    #cv2.waitKey(1)
    return crop_bounding_box(image, mask, min, max, offset)

def find_bright_spots(image):
    '''
    min/max contour area is set as function is only used to find an LED
    '''
    min = 100
    max = 325
    offset = 35
    #https://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/
    #to detect brightest regions in an image convert image to grayscale and smoothing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 11)
    '''
    reveal brightest region by applying threshold
    - any pixel p >= 180 is set to 255 (white)
    - pixels p < 180 are set to 0 (black)
    '''
    filtered = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)[1]
    #cv2.imshow("threshold", filtered)
    #perform erosions and dilations to remove small blobs of noise from threshold image
    #filtered = cv2.erode(filtered, None, iterations=2)
    filtered = cv2.dilate(filtered, None, iterations=2)
    return crop_bounding_box(image, filtered, min, max, offset)

def crop_bounding_box(original, filtered, minval, maxval, offset):
    _, contours, _ = cv2.findContours(filtered, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #apply threshold for contours such that it is range between the minimum and maximum area
    contours = list(filter(lambda c: cv2.contourArea(c) >= minval and cv2.contourArea(c) <= maxval, contours))
    candidates = []
    for c in contours:
        (x,y,w,h) = cv2.boundingRect(c)
        # set the bounding box to be in range of the frame
        y_top = max(0, y-offset)
        y_bot = min(480, y+h+offset)
        x_left = min(640, x+w+offset)
        x_right = max(0, x-offset)
        contour = original[y_top:y_bot, x_right:x_left, :]
        candidates.append(contour)
        #use to display current contour bounding box
        clone = original.copy()
        cv2.rectangle(clone, (x,y), (x+w,y+h), (0,0,255), 2)
        #cv2.rectangle(clone, (x_right,y_top), (x_left,y_bot), (255,0,0), 2)

        #cv2.imshow("bounding box", clone)
        #cv2.waitKey(1)
        #print cv2.contourArea(c)
    return candidates

if __name__ == '__main__':
    vs = PiCamVideoStream().start()
    time.sleep(2.0)
    fps = FPS().start()
    try:
        #while True:
        for i in range(1):
            image = vs.read()
            cv2.imshow('raw',image)
            cv2.imwrite('raw.png', image)
            cv2.waitKey(1)
            image = image[0:240, 320:640, :]    # crop raw image to show only top right quarter
            red_contours = find_red(image, 1800, 5000)
            (winW, winH) = (70, 70)
            print(len(red_contours))
            for img in red_contours:
                for (x, y, window) in sliding_window(img, stepSize=35, windowSize=(winW, winH)):
                    if window.shape[0] != winH or window.shape[1] != winW:
                        continue
                    ss_hit = detect(img[y:y+winH, x:x+winW, :])
                    if(ss_hit):
                        print "found stop sign"
                    else:
                        print "no red light"
                    fps.update()

    except KeyboardInterrupt:
        pass    
    fps.stop()    
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    cv2.destroyAllWindows()
    vs.stop()
