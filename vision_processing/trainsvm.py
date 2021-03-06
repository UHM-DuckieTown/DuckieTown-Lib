import sys, os
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
    for train_image in train_images:
        #open image
        im_gray = cv2.imread(train_image, 0)
        
        #set pts & radius
        radius = 1
        no_points = 8
        
        #get lbp image
        lbp = local_binary_pattern(im_gray, no_points, radius, method='uniform')
        x = lbp.ravel()
        
        #set default hist
        hist, _ = np.histogram(x,bins = (no_points+2), range =(0,no_points+2), density = True)
        lbpset.append(list(hist))

#Get Training Images
ssPosSet = cvutils.imlist("/home/pi/DuckieTown-Lib/features/dataset/ss_positives/")
negSet = cvutils.imlist("/home/pi/DuckieTown-Lib/features/dataset/negatives/")
lbpset = []
labels = [0]*len(negSet)+[1]*len(ssPosSet)
lbp(negSet, lbpset)
lbp(ssPosSet, lbpset)

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
joblib.dump(clf_grid, "clf_stop_sign")
