from sklearn.metrics import accuracy_score
from joblib import load
from pisvm import lbp
import numpy as np
import os
import csv
import sys
import itertools
from PIL import Image

def stopSignDetect(image):
    '''
    modified version of stopSignDetect to return hit or miss in binary form
    :param numpy array image:  3d RGB numpy array
    :return: detected as 1, not detected as 0
    '''
    conf = clf.predict_proba([lbp(image)])[0][1]
    if (conf > 0.7):
        return (1, conf)
    else:
        return (0, conf)	

if __name__ == "__main__":
    OUTPUT_FILE = sys.argv[1] + '.csv'            # create unique filename
    POS_DS_PATH = "dataset/benchmark_p/"
    NEG_DS_PATH = "dataset/benchmark_n/"
    
    POS_DATASET = [POS_DS_PATH+pic for pic in os.listdir(POS_DS_PATH)]
    NEG_DATASET = [NEG_DS_PATH+pic for pic in os.listdir(NEG_DS_PATH)]
    
    clf = load("clf_grid_Stop")
    outfile = open(OUTPUT_FILE, 'a')
    csvfile = csv.writer(outfile)
    csvfile.writerow(['filename', 'expected value', 'predicted value', 'true-pos conf'])

    predicted = []
    confidence = []
    expected = [1 for _ in range(len(POS_DATASET))] + [0 for _ in range(len(NEG_DATASET))]
    
    for pic in itertools.chain(POS_DATASET, NEG_DATASET):
        image = Image.open(pic)				# open *.png with PIL
	arr = np.array(image, dtype='uint8')            # convert *.png to 3d RGB numpy array
        pred, conf = stopSignDetect(arr)
        predicted.append(pred)
        confidence.append(conf)

    for filename, exp, pred, conf in zip(itertools.chain(POS_DATASET, NEG_DATASET), expected, predicted, confidence):
        csvfile.writerow([filename, exp, pred, conf])
    
    print "saved to: " + OUTPUT_FILE
    csvfile.writerow(["score", accuracy_score(expected, predicted)])        # print fraction of correctly classified samples
    outfile.close()
