from __future__ import division
#from shapedetector import ShapeDetector
import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin
import imutils

def find_red(image):
    min = 900     # contour has to have at least 30x30 px area
    max = 1000000000
    #cv2.imshow("image", image)
    image_blur = cv2.medianBlur(image, 21)
    #cv2.imshow("image_blur", image_blur)
    #cv2.waitKey(0)

    #hsv - sepparates color from brightness
    image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

    #filter by color range
    #filter out black
    lower = np.array([0,100,100])
    upper = np.array([20,255,255])
    mask = cv2.inRange(image_blur_hsv, lower, upper)
    return crop_bounding_box(image, mask, min, max)

def find_bright_spots(image):
    min = 50
    max = 250
    #https://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/
    #to detect brightest regions in an image convert image to grayscale and smoothing
    #cv2.imshow("original", image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 11)
    cv2.imshow("blurred", blurred)
    '''
    reveal brightest region by applying threshold
    - any pixel p >= 200 is set to 255 (white)
    - pixels p < 200 are set to 0 (black)
    '''
    filtered = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)[1]
    #cv2.imshow("threshold", filtered)
    #perform erosions and dilations to remove small blobs of noise from threshold image
    #filtered = cv2.erode(filtered, None, iterations=2)
    filtered = cv2.dilate(filtered, None, iterations=2)
    cv2.imshow("filtered", filtered)
    cv2.waitKey(20)
    return crop_bounding_box(image, filtered, min, max)

def crop_bounding_box(original, filtered, min, max):
    _, contours, _ = cv2.findContours(filtered, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #apply threshold for contours such that it has minimum area
    contours = list(filter(lambda c: cv2.contourArea(c) >= min and cv2.contourArea(c) <= max, contours))
    candidates = []
    for c in contours:
        (x,y,w,h) = cv2.boundingRect(c)
        candidates.append(original[y:y+h, x:x+w, :])

        #use to display current contour bounding box
        clone = original.copy()
        cv2.rectangle(clone, (x,y), (x+w,y+h), (255,0,0), 2)
        cv2.imshow("bounding box", clone)
        cv2.waitKey(0)
    return candidates
'''
#test run
image = cv2.imread('dataset/fullsize_0.png')
result = find_shape(image)
cv2.waitKey(0)
'''
