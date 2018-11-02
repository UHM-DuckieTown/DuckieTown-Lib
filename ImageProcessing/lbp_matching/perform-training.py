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

# List for storing the LBP Histograms, address of images and the corresponding label 
X_test = []
X_name = []
y_test = []


#itterate through train images
for train_image in train_images:
    im = cv2.imread(train_image)
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    radius = 3
    no_points = 8 * radius
    lbp = local_binary_pattern(im_gray, no_points, radius, method='uniform')
    x = itemfreq(lbp.ravel())
    # Normalize the histogram
    hist = x[:, 1]/sum(x[:, 1])

    #show histogram
    plt.hist(hist, density=True, bins=30)
    plt.show()
    cv2.waitKey(33)


    # Image Path
    X_name.append(train_image)
    print 'train_image: ' + str(train_image)
    # Hist Values
    X_test.append(hist)
    print 'x_name: ' + str(hist)
    # Key Number
    print 'y_test: ' + str(train_dic[os.path.split(train_image)[1]])
    y_test.append(train_dic[os.path.split(train_image)[1]])

# Save Python Data
joblib.dump((X_name, X_test, y_test), "lbp.pkl", compress=3)
    
# Display the training images
# nrows = 2
# ncols = 3
# fig, axes = plt.subplots(nrows,ncols)
# for row in range(nrows):
#     for col in range(ncols):
#         axes[row][col].imshow(cv2.imread(X_name[row*ncols+col]))
#         axes[row][col].axis('off')
#         axes[row][col].set_title("{}".format(os.path.split(X_name[row*ncols+col])[1]))

# Convert to numpy and display the image
# fig.canvas.draw()
# im_ts = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
# im_ts = im_ts.reshape(fig.canvas.get_width_height()[::-1] + (3,))
# cv2.imshow("Training Set", im_ts)
# cv2.waitKey()
