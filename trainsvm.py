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


# print lbpset

# test_size: split data to train and test on 80-20 ratio (default is 75-25)
# random_state: decides split of which files to use for train and test; use 0 or any int for consistent RNG outcome sequence
#X is the array of the points while Y is the label of whether it's true or not
X_train, X_test, y_train, y_test = train_test_split(lbpset, labels, test_size = 0.2, random_state=0)

# Parameter Grid
#param_grid = {'C': [0.1, 1], 'gamma': [1, 0.1, 0.01, 0.001, 0.00001, 10]}
#C_range = np.logspace(-2, 10, 13)
#gamma_range = np.logspace(-9, 3, 13)
#param_grid = dict(gamma=gamma_range, C=C_range)


param_grid = {'C': [200, 3000, 40000], 'gamma': [200, 3000, 40000]}

# Make grid search classifier
clf_grid = GridSearchCV(svm.SVC(probability=True, kernel='poly'), param_grid, verbose=1)

#clf_grid.probability = True

# Train the classifier
clf_grid.fit(X_train, y_train)


print("Best Parameters:\n", clf_grid.best_params_)
print("Best Estimators:\n", clf_grid.best_estimator_)
joblib.dump(clf_grid, "clf_grid_Stop")
