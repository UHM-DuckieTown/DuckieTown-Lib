import cv2
import numpy as np

__all__ = ['getColor', 'contour']
def getColor(image):
        image_blur = cv2.GaussianBlur(image, (7,7), 0)
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        red = np.uint8([[[0,0,255]]])
        hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)


        lowerRed = np.array([160,20,70])
        upperRed = np.array([190,255,255])

        mask = cv2.inRange(image_hsv, lowerRed, upperRed)
        output = cv2.bitwise_and(image,image, mask = mask)
        #output = cv2.cvtColor(output, cv2.COLOR_HSV2RGB)
        
        #cv2.imshow("images",np.hstack([image, output]))

        contour(image)

def contour(image):
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_blur = cv2.GaussianBlur(image_gray, (7,7), 0)
        ret, thresh = cv2.threshold(image_blur, 200, 255, cv2.THRESH_BINARY) 
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(thresh,contours,-1,(0,255,0),8)
        cv2.imshow("contour", thresh)
