import cv2
import os
from skimage.feature import local_binary_pattern
from scipy.stats import itemfreq
from sklearn.preprocessing import normalize
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.externals import joblib
import argparse as ap
import cvutils

#load training result histograms
X_name, X_test, y_test = joblib.load("lbp.pkl")

test_dic = {}

# Dict containing scores
results_all = {}

video = '../ball.avi'

camera = cv2.VideoCapture(video)

while True:
    ret, im = camera.read()

    if not ret:
        break
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    radius = 3
    no_points = 8 * radius
    lbp = local_binary_pattern(im_gray, no_points, radius, method='uniform')
    x = itemfreq(lbp.ravel())
    hist = x[:, 1]/sum(x[:, 1])
    results = []
    for index, x in enumerate(X_test):
        score = cv2.compareHist(np.array(x, dtype=np.float32), np.array(hist, dtype=np.float32), cv2.cv.CV_COMP_CHISQR)
        results.append((X_name[index], round(score, 3)))
    results = sorted(results, key=lambda score: score[1])
    for image, score in results:
        print "{} has score {}".format(image, score)