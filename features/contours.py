from __future__ import division
#from shapedetector import ShapeDetector
import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin
import imutils
from random import randint

def find_red(image, min, max, slider, twofeed):
    '''
    min: minimum contour area
    max: maximum contour area
    min/max area are the allowed range for the desired contour being represented -> used to find stop sign and red LED
    '''
    offset = 20
    image_blur = cv2.medianBlur(image, 23)

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

    if slider.value == 4:
        twofeed.put(mask)

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

def take_picture(img):
    img_name = "{}_{}.png".format("ss", randint(0,10000))
    cv2.imwrite(img_name, img)
    print "{} written!".format(img_name)
