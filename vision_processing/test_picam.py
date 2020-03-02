from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2

from filter import FilterPipeline
from classifier import Classifier

import random
import string

def crop_contour(contour, frame):
    x,y,w,h = cv2.boundingRect(contour)
    y_top = max(0, y)
    y_bot = min(480, y+h)
    x_left = min(640, x+w)
    x_right = max(0, x)
    return frame[y_top:y_bot, x_right:x_left, :]

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", type=int, default=-1, help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

# created a *threaded *video stream, allow the camera sensor to warmup, and start the FPS counter
print("starting up...")
vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()

# initialize image filtering pipeline
fp = FilterPipeline()

# initialize classifier
clf = Classifier()

# loop over some frames...this time using the threaded stream
try:
    while(1):
        # grab the frame from the threaded video stream and resize i to have a maximum width of 400 pixels
        frame = vs.read()
        display_frame = imutils.resize(frame, height=frame.shape[0], width=frame.shape[1])
        contours = fp.process(frame)
        print(len(contours))
        for c in contours:
            # check to see if the frame should be displayed to our screen
            x,y,w,h = cv2.boundingRect(c)
            y_top = max(0, y)
            y_bot = min(480, y+h)
            x_left = min(640, x+w)
            x_right = max(0, x)
            dclone = display_frame.copy()
            clone = frame.copy()
            cv2.rectangle(clone, (x_right,y_top), (x_left,y_bot), (255,0,0), 2)
            cv2.rectangle(dclone, (x_right,y_top), (x_left,y_bot), (255,0,0), 2)
            cropped = frame[y_top:y_bot, x_right:x_left, :]
            
            # crop out contours        
            contour = crop_contour(c, frame)
            
            '''
            imgname = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(12)])
            cv2.imwrite("{}.png".format(imgname), contour)
            print("saved {}.png",imgname)
            '''
            
            is_detected, pos_conf = clf.detect_stop_sign(contour)
            if is_detected:
                cv2.imshow("bounding box on frame", dclone)
                print(pos_conf)
                cv2.waitKey(1)
                pass
        cv2.imshow("display frame", display_frame)
        cv2.waitKey(1)
        # update the FPS counter
        fps.update()

except KeyboardInterrupt:
    pass

# stop the timer and display FPS information
fps.stop()
#print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
