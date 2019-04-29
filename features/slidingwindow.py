import numpy as np
import cv2
from PIL import Image
import os
import time
from pisvm import detect
import contours
import sys
import multiprocessing

def sliding_window(image, stepSize, windowSize):
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

def img_proc(d,flag):
    while True:
        image = d['image'] 
        #cv2.imshow("raw", image)
        #cv2.waitKey(5)
        image = image[0:240, 320:640, :]    # crop raw image to show only top right quarter
        red_contours = contours.find_red(image, 2500, 5000)
        #red_contours = []
        #light_contours = contours.find_bright_spots(image)
        light_contours= []
        (winW, winH) = (70, 70)
        #start_time = time.time()
        #print "there are {} contours".format(len(red_contours) + len(light_contours))
        #cv2.imshow("live", image)
        #cv2.waitKey(1)
        for img in red_contours + light_contours:
            for (x, y, window) in sliding_window(img, stepSize=35, windowSize=(winW, winH)):
                if window.shape[0] != winH or window.shape[1] != winW:
                    continue
                ss_hit, tl_hit = detect(img[y:y+winH, x:x+winW, :], flag)
                if(ss_hit):
                    print "found stop sign"
                elif(tl_hit):
                    print "red light"
                else:
                    print "no red light"
                #use to show sliding window
                #clone = image.copy()
                #cv2.rectangle(clone, (x,y), (x + winW, y + winH), (0, 255, 0), 2)
                #cv2.imshow('Window', clone)
                #cv2.waitKey(1)
                #time.sleep(0.025)
        #print("---- image processed in {} seconds".format(time.time()-start_time))
