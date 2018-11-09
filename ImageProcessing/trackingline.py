import numpy as np
import cv2
from picamera import PiCamera
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from picamera.array import PiRGBArray
global rightspeed
rightspeed = 95
global leftspeed
leftspeed = 105
def linetracking(raw):
    cv2.imshow('raw',raw)
    raw = raw[300:480,0:480]
    frame = cv2.GaussianBlur(raw, (5, 5), 0)
    Sum = 0
    numx = 0
    avg = 0

    #road = raw[ROI_road_offset:window_height, 0:window_width]

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    min_yellow = np.array([0, 64, 236])
    max_yellow = np.array([32, 255, 255])
    upper = np.array([0, 0, 255])
    lower = np.array([0, 0, 255])
    mask1 = cv2.inRange(hsv, lower, upper)
    #cv2.imshow("white mask", mask1)


    mask2 = cv2.inRange(hsv, min_yellow, max_yellow)
    #mask = cv2.bitwise_or(mask2, mask1)
    if np.all(cv2.bitwise_not(mask2)) == False:
        mask = mask2
        yellow = True
    else:
        mask = mask1
	yellow = False

    cv2.imshow(" mask", mask)
    masked_img = cv2.bitwise_and(hsv, hsv, mask=mask)
    H, S, V = cv2.split(masked_img)
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    #road = edges[260:360, 0:480]

    lines = cv2.HoughLinesP(edges, 1, np.pi/180,20, minLineLength= 1, maxLineGap=1)
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
    cv2.waitKey(20)
    #if cv2.waitKey(20) & 0xFF == ord('q'):
        #break
    return yellow,avg

def position_controller(kp, target, actual):
    error = target-actual
    #errorD = error - old_error
    #global old_error
    #old_error = error
    #print 'Error = ',error
    if abs(error) < 5:
        #do nothing
        return int(0)
    else:
        adjustment = kp*error
        return int(adjustment)

def position_p(camera, capture):
    window_width = 480
    window_height = 360
    for frame in camera.capture_continuous(capture, format='bgr', use_video_port=True):
       #ret, raw = cap.read()
       image = capture.array
       raw = cv2.resize(image, (window_width, window_height))
       Kp = 0.15
       yellow,avg = linetracking(raw)
       #130 for yellow line, 450 for white
       if yellow:
           threshold = 105

       else:
           threshold = 430
       global rightspeed
       global leftspeed
       rightspeed = int(95 + position_controller(Kp,threshold,avg))
       leftspeed = int(105 - position_controller(Kp,threshold,avg))

       if rightspeed > 255:
           rightspeed = 255

       elif rightspeed < 0:
           rightspeed = 0

       if leftspeed > 255:
           leftspeed = 255

       elif rightspeed < 0:
           rightspeed = 0
       capture.truncate(0)
       #return rightspeed, leftspeed
