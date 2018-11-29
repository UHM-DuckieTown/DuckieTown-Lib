import sys, os
#import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV
import cv2
from skimage.feature import local_binary_pattern
from scipy.stats import itemfreq
import numpy as np
import joblib
import argparse as ap
import cvutils
import csv
import matplotlib.pyplot as plt
def lbp(train_images, lbpset):
    #itterate through train images
    for train_image in train_images:
        #open image
        im = cv2.imread(train_image)
        #convert to grayscale image
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #set pts & radius
        radius = 1
        no_points = 8
        #get lbp image
        lbp = local_binary_pattern(im_gray, no_points, radius, method='uniform')
        #cv2.imshow(lbp)
        #sort by freq
        x = lbp.ravel()
        #print(x)
        # Normalize values
        #hist = x[:, 1]/sum(x[:, 1])
        #set default hist
        hist, _ = np.histogram(x,bins = (no_points+2), range =(0,no_points+2), density = True)
        #plt.hist(x, bins='auto')
        #plt.show()
        #print(list(hist))
        #print(sum(list(hist)))
        #add values to set
        lbpset.append(list(hist))



# ARGUMENTS
parser = ap.ArgumentParser()
parser.add_argument("-p", "--posSet", help="Path to Positive Set", required="True")
parser.add_argument("-n", "--negSet", help="Path to Negitive Set", required="True")
args = vars(parser.parse_args())

#Get Training Images
posSet = cvutils.imlist(args["posSet"])
negSet = cvutils.imlist(args["negSet"])
lbpset = []
labels = [0]*len(negSet)+[1]*len(posSet)
lbp(negSet, lbpset)
lbp(posSet, lbpset)

clf=joblib.load("clf_grid_Stop")

for test in lbpset:
    print(clf.predict([test]))
