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

nou = []
labels = [0]*9
# ARGUMENTS
parser = ap.ArgumentParser()
parser.add_argument("-t", "--trainingSet", help="Path to Training Set", required="True")
parser.add_argument("-l", "--imageLabels", help="Path to Image Label Files", required="True")
args = vars(parser.parse_args())

#Get Training Images Paths
train_images = cvutils.imlist(args["trainingSet"])

#Make Dic to store files and keys
train_dic = {}
with open(args['imageLabels'], 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        train_dic[row[0]] = int(row[1])
#itterate through train images
for train_image in train_images:
    #cv2.imread(train_image)
    #
    im = cv2.imread(train_image)
    #im = np.array(im, dtype=np.uint8)
#    cv2.imshow('test',im)
    im_gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    radius = 1
    no_points = 8 * radius
    lbp = local_binary_pattern(im_gray, no_points, radius, method='uniform')
    #y = lbp.ravel()
    #print y
    x = itemfreq(lbp.ravel())
    #print x
    # Normalize the histogram
    hist = x[:, 1]/sum(x[:, 1])
    #    print(hist)
    hist = np.histogram(hist,bins =20, range =(0,1))
    #x.append(list(hist[0]))
    #print(list(hist[0]))

    #x = np.concatenate(x,a, axis=1)
    nou.append(list(hist[0]))
        #for i in hist:
        # print i[0]
        #np.append(x,i[0])
print nou

# Split data to train and test on 80-20 ratio
#X is the array of the points while Y is the label of whether it's true or not
X_train, X_test, y_train, y_test = train_test_split(nou, labels, test_size = 0.2, random_state=0)

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
