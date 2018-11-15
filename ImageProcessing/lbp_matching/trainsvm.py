import sys, os
#import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV
import cv2
from skimage.feature import local_binary_pattern
from scipy.stats import itemfreq
import numpy as np
from sklearn.externals import joblib
import argparse as ap
import cvutils
import csv

def lbp(train_images, lbpset):
    #itterate through train images
    for train_image in train_images:
        #open image
        im = cv2.imread(train_image)
        #convert to grayscale image
        im_gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        #set pts & radius
        radius = 1
        no_points = 8 * radius
        #get lbp image
        lbp = local_binary_pattern(im_gray, no_points, radius, method='uniform')
        #sort by freq
        x = itemfreq(lbp.ravel())
        # Normalize values
        hist = x[:, 1]/sum(x[:, 1])
        #set default hist
        hist = np.histogram(hist,bins =20, range =(0,1))
        #print(list(hist[0]))
        #add values to set
        lbpset.append(list(hist[0]))



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

# Split data to train and test on 80-20 ratio
#X is the array of the points while Y is the label of whether it's true or not
X_train, X_test, y_train, y_test = train_test_split(lbpset, labels, test_size = 0.2, random_state=0)

#print("Displaying data. Close window to continue")
# Plot data
#plot_data(X_train, y_train, X_test, y_test)

#print("Training SVM ...")
# make a classifier
#clf = svm.SVC(C = 10.0, kernel='rbf', gamma=0.1)

# Train classifier
#clf.fit(X_train, y_train)

# Make predictions on unseen test data
#clf_predictions = clf.predict(X_test)

#print("Displaying decision function. Close window to continue")
# Plot decision function on training and test data
#plot_decision_function(X_train, y_train, X_test, y_test, clf)

# Grid Search
#print("Performing grid search ... ")

# Parameter Grid
param_grid = {'C': [0.1, 1, 10, 100], 'gamma': [1, 0.1, 0.01, 0.001, 0.00001, 10]}

# Make grid search classifier
clf_grid = GridSearchCV(svm.SVC(), param_grid, verbose=1)

# Train the classifier
clf_grid.fit(X_train, y_train)

# clf = grid.best_estimator_()
print("Best Parameters:\n", clf_grid.best_params_)
print("Best Estimators:\n", clf_grid.best_estimator_)
joblib.dump(clf_grid, "clf_grid")
#print("Displaying decision function for best estimator. Close window to continue.")
# Plot decision function on training and test data
#plot_decision_function(X_train, y_train, X_test, y_test, clf_grid)
