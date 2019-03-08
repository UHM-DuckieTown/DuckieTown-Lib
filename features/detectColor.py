from __future__ import division
from shapedetector import ShapeDetector
import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin
import imutils


def find_shape(image):
    # convert color scheme
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    image_blur = cv2.GaussianBlur(image, (7,7), 0)
    
    #hsv - sepparates color from brightness
    image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

    # filter by color range
    # filter out black
    lower = np.array([100,50,50])
    upper = np.array([130,255,255])
    mask = cv2.inRange(image_blur_hsv, lower, upper)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    print "num contours detected: {}".format(len(contours))
    
    if contours:
        c= max(contours, key = cv2.contourArea)
    
        min_y, min_x, _ = image_blur_hsv.shape
        max_x = max_y = 0
        (x,y,w,h) = cv2.boundingRect(c)
    
        cv2.rectangle(image, (x,y), (x+w,y+h), (255, 0, 0), 2)  
        
    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    
    return image

image = cv2.imread('dataset/positives/stopsign_47.png')
result = find_shape(image)
cv2.waitKey(0)
