import cv2
import numpy as np
import math

class Shapes() :
    def __init__(self, img):
        self.img = img

    def maskImage(self):
        lowerBound = np.array([0,0,0], dtype=np.uint8)
        upperBound = np.array([15,15,15], dtype=np.uint8)
        mask = cv2.inRange(self.img, lowerBound, upperBound)
        cv2.imshow("masked image", mask)

        (flags, contours, h) = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contours

img = cv2.imread("shapetest.png")

shapes = Shapes(img)

contours = shapes.maskImage()
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()