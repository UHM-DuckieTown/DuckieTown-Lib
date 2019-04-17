from __future__ import division
#from shapedetector import ShapeDetector
import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin
import imutils

def find_red(image, min, max):
    #min = 900     # contour has to have at least 30x30 px area
    #max = 1000000000
    offset = 0
    #view mode
    #cv2.imshow("image", image)
    image_blur = cv2.medianBlur(image, 15)
    cv2.imshow("image_blur", image_blur)
    #cv2.waitKey(0)

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

    #view mode
    #cv2.imshow("red mask", mask)
    return crop_bounding_box(image, mask, min, max, offset)

def find_bright_spots(image):
    min = 100
    max = 325
    offset = 35
    #https://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/
    #to detect brightest regions in an image convert image to grayscale and smoothing
    cv2.imshow("original", image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 11)
    #cv2.imshow("blurred", blurred)
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
    #cv2.waitKey(20)
    return crop_bounding_box(image, filtered, min, max, offset)

def crop_bounding_box(original, filtered, minval, maxval, offset):
    _, contours, _ = cv2.findContours(filtered, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #apply threshold for contours such that it has minimum area
    contours = list(filter(lambda c: cv2.contourArea(c) >= minval and cv2.contourArea(c) <= maxval, contours))
    candidates = []
    for c in contours:
        (x,y,w,h) = cv2.boundingRect(c)
        y_top = max(0, y-offset)
        y_bot = min(480, y+h+offset)
        x_left = min(640, x+w+offset)
        x_right = max(0, x-offset)
        candidates.append(original[y_top:y_bot, x_right:x_left, :])
        #use to display current contour bounding box
        clone = original.copy()
        print cv2.contourArea(c)
        cv2.rectangle(clone, (x,y), (x+w,y+h), (0,0,255), 2)
        cv2.rectangle(clone, (x_right,y_top), (x_left,y_bot), (255,0,0), 2)
        #view mode
        cv2.imshow("bounding box", clone)
        cv2.waitKey(0)
    return candidates
'''
#test run
image = cv2.imread('dataset/fullsize_0.png')
result = find_shape(image)
cv2.waitKey(0)
'''
