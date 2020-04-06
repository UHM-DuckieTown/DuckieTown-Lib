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
import glob

#Get Training Images
ss_set = cvutils.imlist("/home/pi/DuckieTown-Lib/vision_processing/dataset/ss_crop/")
tl_set = cvutils.imlist("/home/pi/DuckieTown-Lib/vision_processing/dataset/tl_crop/")
neg_set = cvutils.imlist("/home/pi/DuckieTown-Lib/vision_processing/dataset/neg_crop/")

labels = np.array([0]*len(neg_set) + [1]*len(ss_set) + [2]*len(tl_set))
img_list = []
for img in neg_set + ss_set + tl_set:
    img_list.append(cv2.imread(img,0))

# flatten 3D array to 2D
img_list = np.array(img_list).reshape((1280, 120*640))

# test_size: split data to train and test on 70-30 ratio (default is 75-25)
# random_state: decides split of which files to use for train and test; use 0 or any int for consistent RNG outcome sequence
#X is the array of the points while Y is the label of whether it's true or not

print(img_list.shape)
print(labels.shape)
X_train, X_test, y_train, y_test = train_test_split(img_list, labels, test_size = 0.25, random_state=0)

param_grid = [{'kernel': ('linear', 'poly'), 'C': [0.001, 0.1, 1, 100, 1000], 'gamma': [1000, 10000, 100000]}]
clf_grid = GridSearchCV(svm.SVC(probability=True, decision_function_shape='ovr'), param_grid, verbose=1)
clf_grid.fit(X_train, y_train)


# Predict the response for test dataset
y_pred = clf_grid.predict(X_test)
print("Best Parameters:\n", clf_grid.best_params_)
print("Best Estimators:\n", clf_grid.best_estimator_)
print("Classification accuracy:\n", metrics.accuracy_score(y_test, y_pred))
joblib.dump(clf_grid, "test")
