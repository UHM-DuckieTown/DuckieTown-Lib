import sys, os
#import matplotlib.pyplot as plt
from sklearn import svm, metrics
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
        im_gray = cv2.imread(train_image, 0)
        #im = cv2.imread(train_image)
        #convert to grayscale image
        #im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
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

def orb_matcher(training_images):
    test_image = cv2.imread("stop_sign.png", cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create(scoreType=cv2.ORB_FAST_SCORE)
    kp1, des1 = orb.detectAndCompute(img1, None)
    feature_list = []

    for image in training_images:
        img_gray = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        kp2, des2 = orb.detectAndCompute(img2, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key = lambda x:x.distance)
        feature_list.append(list(matches))

#Get Training Images
ssPosSet = cvutils.imlist("dataset/ss_positives/")
tlPosSet = cvutils.imlist("dataset/tl_positives/")
negSet = cvutils.imlist("dataset/negatives/")
lbpset = []
labels = [0]*len(negSet)+[1]*len(ssPosSet)+[2]*len(tlPosSet)
lbp(negSet, lbpset)
lbp(ssPosSet, lbpset)
lbp(tlPosSet, lbpset)

# test_size: split data to train and test on 70-30 ratio (default is 75-25)
# random_state: decides split of which files to use for train and test; use 0 or any int for consistent RNG outcome sequence
#X is the array of the points while Y is the label of whether it's true or not
X_train, X_test, y_train, y_test = train_test_split(lbpset, labels, test_size = 0.3, random_state=0)

# Parameter Grid
#param_grid = {'C': [0.1, 1], 'gamma': [1, 0.1, 0.01, 0.001, 0.00001, 10]}
#C_range = np.logspace(-2, 10, 13)
#gamma_range = np.logspace(-9, 3, 13)
#param_grid = dict(gamma=gamma_range, C=C_range)


param_grid = [{'kernel': ('linear', 'poly'), 'C': [1000], 'gamma': [1000, 10000, 100000]}]

# Make grid search classifier
clf_grid = GridSearchCV(svm.SVC(probability=True), param_grid, verbose=1)

# Train the classifier
clf_grid.fit(X_train, y_train)

# Predict the response for test dataset
y_pred = clf_grid.predict(X_test)

print("Best Parameters:\n", clf_grid.best_params_)
print("Best Estimators:\n", clf_grid.best_estimator_)
print("Classification accuracy:\n", metrics.accuracy_score(y_test, y_pred))
joblib.dump(clf_grid, "clf_grid_Stop")
