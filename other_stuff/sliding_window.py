
# import the necessary packages
import argparse
import time
import cv2
#import imutils
from picamera import PiCamera
from picamera.array import PiRGBArray

def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])
"""
def pyramid(image, scale=1.5, minSize=(30, 30)):
    # yield the original image
    yield image
    
    # keep looping over the pyramid
    while True:
        # compute the new dimensions of the image and resize it
        w = int(image.shape[1] / scale)
        image = imutils.resize(image, width=w)
        
        # if the resized image does not meet the supplied minimum
        # size, then stop constructing the pyramid
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break
        
        # yield the next image in the pyramid
        yield image
# construct the argument parser and parse the arguments
print('1')

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])
"""

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
raw = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

#camera.capture(raw, format="bgr")
for frame in camera.capture_continuous(raw, format='bgr', use_video_port=True):
    image= raw.array
    (winW, winH) = (128, 128)# loop over the image pyramid
    #for resized in pyramid(image, scale=1.5):
    # loop over the sliding window for each layer of the pyramid
    for (x, y, window) in sliding_window(image, stepSize=100, windowSize=(winW, winH)):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != winH or window.shape[1] != winW:
            continue
        # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW, SUCH AS APPLYING A
        # MACHINE LEARNING CLASSIFIER TO CLASSIFY THE CONTENTS OF THE
        # WINDOW

        # since we do not have a classifier, we'll just draw the window
        clone = image.copy()
        cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
        cv2.imshow("Window", clone)
        #print('1')
    cv2.waitKey(1)
    cv2.imshow("Preview", image)
    key = cv2.waitKey(1)
    raw.truncate(0)
    if key == ord('q'):
        break
