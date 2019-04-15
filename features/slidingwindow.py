import numpy as np
import cv2
from PIL import Image
import os
import time
from pisvm import detect
import contours

def sliding_window(image, stepSize, windowSize):
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


def img_proc(q, flag):
    #PIC_PATH = "dataset/fullsize_0.png"
    #image = cv2.imread(PIC_PATH)
    #cv2.imshow('current window', image)


    while True:

        
        image = q.get()
        
        
#enable viewing of original image
#        cv2.imshow("uncropped", image)
#        key = cv2.waitKey(1) & 0xFF

        image = image[0:240, 320:640, :]
        red_contours = contours.find_red(image)
        #red_contours = []
        #light_contours = contours.find_bright_spots(image)
        light_contours= []
        (winW, winH) = (70, 70)
        #start_time = time.time()
        print "there are {} contours".format(len(red_contours))
        for img in red_contours + ['#'] + light_contours:
            if img == '#':
                winH += 70  # change sliding window region to (70, 140) to match traffic light training image dimensions
                continue
            for (x, y, window) in sliding_window(img, stepSize=35, windowSize=(winW, winH)):
                if window.shape[0] != winH or window.shape[1] != winW:
                    continue
                ss_hit, tl_hit = detect(img[y:y+winH, x:x+winW, :], flag)
                if(ss_hit):
                    print "found stop sign"
                else:
                    print "lost stop sign"
                if(tl_hit):
                    print "found traffic light"
                #cv2.waitKey(0)
                #use to show sliding window
                #clone = image.copy()
                #cv2.rectangle(clone, (x,y), (x + winW, y + winH), (0, 255, 0), 2)
                #cv2.imshow('Window', clone)
                #cv2.waitKey(1)
                #time.sleep(0.025)
        #print("---- image processed in {} seconds".format(time.time()-start_time))
