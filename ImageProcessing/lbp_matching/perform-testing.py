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

parser = ap.ArgumentParser()
parser.add_argument("-t", "--testingSet", help="Path to Testing Set", required="True")
parser.add_argument("-l", "--imageLabels", help="Path to Image Label Files", required="True")
args = vars(parser.parse_args())

X_name, X_test, y_test = joblib.load("lbp.pkl")

test_images = cvutils.imlist(args["testingSet"])
test_dic = {}
with open(args["imageLabels"], 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        test_dic[row[0]] = int(row[1])

# Dict containing scores
results_all = {}

for test_image in test_images:
    print "\nCalculating Hist:  " + str(test_image)
    im = cv2.imread(test_image)
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
    results_all[test_image] = results
    print "Scores: " + str(test_image)
    for image, score in results:
        print "{} has score {}".format(image, score)

# for test_image, results in results_all.items():
#     # Read the image
#     im = cv2.imread(test_image)
#     # Display the results
#     nrows = 2
#     ncols = 3
#     fig, axes = plt.subplots(nrows,ncols)
#     fig.suptitle("** Scores for -> {}**".format(test_image))
#     for row in range(nrows):
#         for col in range(ncols):
#             axes[row][col].imshow(cv2.imread(results[row*ncols+col][0]))
#             axes[row][col].axis('off')
#             axes[row][col].set_title("Score {}".format(results[row*ncols+col][1]))
#     fig.canvas.draw()
#     im_ts = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
#     im_ts = im_ts.reshape(fig.canvas.get_width_height()[::-1] + (3,))
#     cv2.imshow("** Query Image -> {}**".format(test_image), im)
#     cv2.imshow("** Scores for -> {}**".format(test_image), im_ts)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
