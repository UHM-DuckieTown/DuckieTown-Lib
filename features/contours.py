from __future__ import division
import pytesseract
from PIL import Image
#from shapedetector import ShapeDetector
import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin
import imutils
from random import randint
import argparse
ap=argparse.ArgumentParser()
ap.add_argument("-east", "--east", type=str,help="path to input EAST text detector", default="frozen_east_text_detection.pb")
ap.add_argument("-c", "--min-confidence", type=float, default=0.5,help="minimum probability required to inspect a region")
args = vars(ap.parse_args())

def decode_predictions(scores, geometry):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]   
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability,
            # ignore it
            if scoresData[x] < args["min_confidence"]:
                continue
            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            # use the geometry volume to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
    # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)

def find_red(image, min, max, slider, twofeed):
    '''
    min: minimum contour area
    max: maximum contour area
    min/max area are the allowed range for the desired contour being represented -> used to find stop sign and red LED
    '''
    offset = 20
    image_blur = cv2.medianBlur(image, 23)

    #hsv - sepparates color from brightness
    image_blur_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #lower mask (0-10)
    lower = np.array([0,50,50])
    upper = np.array([10,255,255])
    mask0 = cv2.inRange(image_blur_hsv, lower, upper)

    #upper mask (170-180)
    lower = np.array([170,50,50])
    upper = np.array([180,255,255])
    mask1 = cv2.inRange(image_blur_hsv, lower, upper)

    #join mask
    mask = mask0+mask1

    if slider.value == 4:
        twofeed.put(mask)

    cv2.imshow("live", image)
    #cv2.imshow("red mask", mask)
    cv2.waitKey(1)
    return crop_bounding_box(image, mask, min, max, offset)

def find_bright_spots(image):
    '''
    min/max contour area is set as function is only used to find an LED
    '''
    min = 100
    max = 325
    offset = 35
    #https://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/
    #to detect brightest regions in an image convert image to grayscale and smoothing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 11)
    '''
    reveal brightest region by applying threshold
    - any pixel p >= 180 is set to 255 (white)
    - pixels p < 180 are set to 0 (black)
    '''
    filtered = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("threshold", filtered)
    #perform erosions and dilations to remove small blobs of noise from threshold image
    #filtered = cv2.erode(filtered, None, iterations=2)
    filtered = cv2.dilate(filtered, None, iterations=2)
    return crop_bounding_box(image, filtered, min, max, offset)

def crop_bounding_box(original, filtered, minval, maxval, offset):
    _, contours, _ = cv2.findContours(filtered, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #apply threshold for contours such that it is range between the minimum and maximum area
    contours = list(filter(lambda c: cv2.contourArea(c) >= minval and cv2.contourArea(c) <= maxval, contours))
    candidates = []
    for c in contours:
        (x,y,w,h) = cv2.boundingRect(c)
        # set the bounding box to be in range of the frame
        y_top = max(0, y-offset)
        y_bot = min(480, y+h+offset)
        x_left = min(640, x+w+offset)
        x_right = max(0, x-offset)
        contour = original[y_top:y_bot, x_right:x_left, :]
        candidates.append(contour)
        #use to display current contour bounding box
        clone = original.copy()
        cv2.rectangle(clone, (x,y), (x+w,y+h), (0,0,255), 2)
        #cv2.rectangle(clone, (x_right,y_top), (x_left,y_bot), (255,0,0), 2)

        cv2.imshow("bounding box", clone)
        cv2.imshow("cropped", contour)
        #cv2.waitKey(1)
        #print cv2.contourArea(c)
        img = contour
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    
        lower_white = np.array([96,0,142])
        upper_white = np.array([180, 50, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        img = cv2.bitwise_and(img , img, mask=mask)
        
        #img = cv2.resize(img,(0,0),fx=3,fy=3)
        #img = cv2.GaussianBlur(img,(11,11),0)
        #img = cv2.medianBlur(img,9)

        # load the input image and grab the image dimensions
        image = img
        orig = image.copy()
        (origH, origW) = image.shape[:2]
        # set the new width and height and then determine the ratio in change
        # for both the width and height
        (newW, newH) = (320, 320)
        rW = origW / float(newW)
        rH = origH / float(newH)
        # resize the image and grab the new image dimensions
        image = cv2.resize(image, (newW, newH))
        (H, W) = image.shape[:2]
        # define the two output layer names for the EAST detector model that
        # we are interested -- the first is the output probabilities and the
        # second can be used to derive the bounding box coordinates of text
        layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
                "feature_fusion/concat_3"]
        # load the pre-trained EAST text detector
        print("[INFO] loading EAST text detector...")
        net = cv2.dnn.readNet(args["east"])

        # construct a blob from the image and then perform a forward pass of
        # the model to obtain the two output layer sets
        blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
            (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)

        # decode the predictions, then  apply non-maxima suppression to
        # suppress weak, overlapping bounding boxes
        (rects, confidences) = decode_predictions(scores, geometry)
        boxes = non_max_suppression(np.array(rects), probs=confidences)

        # initialize the list of results
        results = []

        # loop over the bounding boxes
        for (startX, startY, endX, endY) in boxes:
            # scale the bounding box coordinates based on the respective
            # ratios
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)
            # in order to obtain a better OCR of the text we can potentially
            # apply a bit of padding surrounding the bounding box -- here we
            # are computing the deltas in both the x and y directions
            dX = int((endX - startX) * 0.05)
            dY = int((endY - startY) * 0.05)
            # apply padding to each side of the bounding box, respectively
            startX = max(0, startX - dX)
            startY = max(0, startY - dY)
            endX = min(origW, endX + (dX * 2))
            endY = min(origH, endY + (dY * 2))
            # extract the actual padded ROI
            roi = orig[startY:endY, startX:endX]
            # in order to apply Tesseract v4 to OCR text we must supply
            # (1) a language, (2) an OEM flag of 4, indicating that the we
            # wish to use the LSTM neural net model for OCR, and finally
            # (3) an OEM value, in this case, 7 which implies that we are
            # treating the ROI as a single line of text
            config = ("-l eng --oem 1 --psm 7")
            text = pytesseract.image_to_string(roi, config=config)
            # add the bounding box coordinates and OCR'd text to the list
            # of results
            results.append(((startX, startY, endX, endY), text))
            # sort the results bounding box coordinates from top to bottom
        results = sorted(results, key=lambda r:r[0][1])
        # loop over the results
        for ((startX, startY, endX, endY), text) in results:
            # display the text OCR'd by Tesseract
            print("OCR TEXT")
            print("========")
            print("{}\n".format(text))
            # strip out non-ASCII text so we can draw the text on the image
            # using OpenCV, then draw the text and a bounding box surrounding
            # the text region of the input image
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            output = orig.copy()
            cv2.rectangle(output, (startX, startY), (endX, endY),(0, 0, 255), 2)
            cv2.putText(output, text, (startX, startY - 20),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            # show the output image
            cv2.imshow("Text Detection", output)
            cv2.waitKey(1)
        cv2.imshow("mask", mask)
        cv2.imshow("filtered img", img)
        cv2.waitKey(1)

        img = Image.fromarray(img)
        text = pytesseract.image_to_string(img, lang='eng', config = '-l eng --oem 1 --psm 3')
        print("recognized output text: ", text)
    return candidates

def take_picture(img):
    img_name = "{}_{}.png".format("ss", randint(0,10000))
    cv2.imwrite(img_name, img)
    print "{} written!".format(img_name)
