import numpy as np
import cv2
from skimage.feature import local_binary_pattern
from joblib import load
from os import path

class Classifier:
    def __init__(self):
        if path.exists("clf_stop_sign"):
            self.clf = load("clf_stop_sign")
        else:
            self.clf = load("vision_processing/clf_stop_sign")
        self.pos_threshold = 0.95

    def detect_stop_sign(self, image):
        neg_conf, pos_conf = self.clf.predict_proba([self.__lbp(image)])[0]
        return (True, pos_conf) if pos_conf >= self.pos_threshold else (False, pos_conf)

    @staticmethod
    def __lbp(image, radius = 1, no_points = 8):
        #convert to grayscale image
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #set pts & radius
        #circular lbp
        lbp = local_binary_pattern(img_gray, no_points, radius, method='uniform')
        x = lbp.ravel()
        hist, _ = np.histogram(x,bins = (no_points+2), range =(0,no_points+2), density = True)
        return hist
