import numpy as np
import cv2
import time
from picamera.array import PiRGBArray
def position_controller(kp, target, actual):
    error = target-actual
    #print 'Error = ',error
    if abs(error) < 5:
        #do nothing
        return int(0)
    else:
        adjustment = kp*error
        return int(adjustment)

def line_track(camera):
      for frame in camera.capture_continuous(capture, format='bgr', use_video_port=True):
          image = capture.array
          raw = cv2.resize(image, (window_width, window_height))

          frame = cv2.GaussianBlur(raw, (5, 5), 0)
          Sum = 0
          numx = 0
          avg = 0

          hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
          min_yellow = np.array([0, 64, 236])
          max_yellow = np.array([32, 255, 255])
          upper = np.array([0, 0, 255])
          lower = np.array([0, 0, 255])
          mask1 = cv2.inRange(hsv, lower, upper)

          mask2 = cv2.inRange(hsv, min_yellow, max_yellow)
          mask = cv2.bitwise_or(mask2, mask1)
          cv2.imshow(" mask", mask2)
          masked_img = cv2.bitwise_and(hsv, hsv, mask=mask2)
          H, S, V = cv2.split(masked_img)
          edges = cv2.Canny(mask2, 50, 150, apertureSize=3)

          lines = cv2.HoughLinesP(edges, 1, np.pi/180,100, minLineLength= 50, maxLineGap=10)
          if lines is not None:
              for line in lines:
                  x1, y1, x2, y2 = line[0]
                  cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                  cv2.circle(frame, (x1, y1),2,(255,0,0),3)
                  cv2.circle(frame,(x2,y2),2,(255,0,0),3)
                  numx += 2
                  Sum = Sum + x1 + x2
              old_avg = avg
         if numx is not 0:
             avg = Sum/numx
         else:
             avg = old_avg
         cv2.circle(frame,(avg,300),2,(0,0,255),3)
         print 'Average = ', avg
         cv2.imshow('frame', frame)
         cv2.imshow('edges', edges)
