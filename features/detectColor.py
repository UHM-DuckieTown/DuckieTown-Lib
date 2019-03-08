from __future__ import division
from shapedetector import ShapeDetector
import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin
import imutils


def find_shape(image):
    # convert color scheme
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    max_dim = max(image.shape)

    # scale image
    scale = 1
    image = cv2.resize(image, None, fx=scale, fy=scale)
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])

    # smooth image (image, ratio, filter)
    image_blur = cv2.GaussianBlur(resized, (7,7), 0)
    
    #hsv - sepparates color from brightness
    image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

    # filter by color range
    # filter out black
    lowerBlack = np.array([100,50,50])
    upperBlack = np.array([130,255,255])
    mask = cv2.inRange(image_blur_hsv, lowerBlack, upperBlack)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    print "num contours detected: {}".format(len(contours))
    c= max(contours, key = cv2.contourArea)
    
    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape on the image
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        
        
    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    
    return image

image = cv2.imread('shapetest1.png')
result = find_shape(image)
cv2.waitKey(0)
