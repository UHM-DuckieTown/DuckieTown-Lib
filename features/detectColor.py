from __future__ import division
from shapedetector import ShapeDetector
import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin
import imutils

def find_shape(image):
    threshold = 900        # contour has to have at least 30x30 px area
    # convert color scheme
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #cv2.imshow("image", image)
    image_blur = cv2.medianBlur(image, 21)
    cv2.imshow("image_blur", image_blur)
    #cv2.waitKey(0)

    #hsv - sepparates color from brightness
    image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

    # filter by color range
    # filter out black
    lower = np.array([0,100,100])
    upper = np.array([20,255,255])
    mask = cv2.inRange(image_blur_hsv, lower, upper)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []
    contours = list(filter(lambda c: cv2.contourArea(c) >= threshold, contours))
    print "num contours detected: {}".format(len(contours))
    min_y, min_x, _ = image_blur_hsv.shape
    max_x = max_y = 0

    for c in contours:
        print "area is: {}".format(cv2.contourArea(c))
        (x,y,w,h) = cv2.boundingRect(c)
        candidates.append(image[y:y+h, x:x+w, :])
        
        #use to display current contour bounding box
        clone = image.copy()
        cv2.rectangle(clone, (x,y), (x+w,y+h), (255,0,0), 2)
        cv2.imshow("Image", clone)
        cv2.waitKey(0)

    '''
    #use to show bounding box of all contours detected
    if contours:
        c= max(contours, key = cv2.contourArea)

        min_y, min_x, _ = image_blur_hsv.shape
        max_x = max_y = 0

        (x,y,w,h) = cv2.boundingRect(c)
        cv2.rectangle(image, (x,y), (x+w,y+h), (255, 0, 0), 2)
        image = image[y:y+h, x:x+w]

    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    '''

    return candidates
'''
#test run
image = cv2.imread('dataset/fullsize_0.png')
result = find_shape(image)
cv2.waitKey(0)
'''
