import numpy as np
import cv2
from picamera import PiCamera
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from picamera.array import PiRGBArray
#import velocity
global rightspeed
rightspeed = 0
global leftspeed
leftspeed = 0
global camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
global capture
capture = PiRGBArray(camera, size=(640,480))
time.sleep(0.1)
global Position_errorP_v
Position_errorP_v = 0
global Position_old_errorP_v
Position_old_errorP_v = 0
global Position_errorD_v
Position_errorD_v = 0
global Position_errorI_v
Position_errorI_v = 0
global Position_totalError_v
Position_totalError_v = 0
POSITIONP = 0.1
POSITIONI = 0.0000
POSITIOND = 0.0005
POSITIONF = 0
def detect_stop(hsv):
    #cv2.imshow('raw',raw)
    #raw = raw[200:480,0:480]
    #frame = cv2.GaussianBlur(raw, (5, 5), 0)
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #min_yellow = np.array([0, 64, 236])
    #max_yellow = np.array([32, 255, 255])
    upper = np.array([0, 0, 255])
    lower = np.array([0, 0, 255])
    mask1 = cv2.inRange(hsv, lower, upper)
    edges = cv2.Canny(mask1, 50, 150, apertureSize=3)
    #road = edges[260:360, 0:480]

    lines = cv2.HoughLinesP(edges, 1, np.pi/180,20, minLineLength= 200, maxLineGap=1)
   
    print "in detect_stop"
    stop = False
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
	    if (x2-x1) == 0:
	    	continue
            m = (y2-y1)/(x2-x1)
	    print "Slope=",m
            if abs(m) < 0.5:
                stop = True
		return stop
            else:
                stop = False
    #print "Value of stop=",stop
    return stop

def linetracking(raw):
    cv2.imshow('raw',raw)
    raw = raw[200:480,0:480]
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
    #mask3 = cv2.bitwise_or(mask2, mask1)
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

    lines = cv2.HoughLinesP(edges, 1, np.pi/180,20, minLineLength= 10, maxLineGap=1)
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
    stop = detect_stop(hsv)
    #stop = False
    #print 'Average = ', avg
    cv2.imshow('frame', frame)
    cv2.imshow('edges', edges)
    cv2.waitKey(20)
    #if cv2.waitKey(20) & 0xFF == ord('q'):
        #break
    return yellow,avg,stop


def position_controller(target, actual):
    global Position_errorP_v
    Position_errorP_v = target-actual
    global Position_errorI_v
    Position_errorI_v = Position_errorI_v + Position_errorP_v
    global Position_errorD_v
    Position_errorD_v = Position_errorP_v - Position_old_errorP_v
    global Position_totalError_v
    Position_totalError_v = POSITIONP * Position_errorP_v + POSITIONI * Position_errorI_v + POSITIOND *Position_errorD_v + POSITIONF
    global Position_old_errorP_v
    Position_old_errorP_v = Position_errorP_v
    #global old_error
    #old_error = error
    #print 'Error = ',error
    if abs(Position_totalError_v) < 5:
        #do nothing
        return int(0)
    else:
        adjustment = Position_totalError_v
        return int(adjustment)

def position_p():
    window_width = 480
    window_height = 360
    global camera
    global capture
    for frame in camera.capture_continuous(capture, format='bgr', use_video_port=True):
       #ret, raw = cap.read()
       global capture
       image = capture.array
       raw = cv2.resize(image, (window_width, window_height))

       yellow,avg,stop = linetracking(raw)
       #130 for yellow line, 450 for white
       if yellow:
           threshold = 105

       else:
           threshold = 430
       global rightspeed
       global leftspeed
       rightspeed = int(100 + position_controller(threshold,avg))
       leftspeed = int(100 - position_controller(threshold,avg))
       #rightspeed = 100
       #leftspeed = 100
       if rightspeed > 255:
           rightspeed = 255

       elif rightspeed < 0:
           rightspeed = 0

       if leftspeed > 255:
           leftspeed = 255

       elif rightspeed < 0:
           rightspeed = 0
       if stop == True:
           leftspeed = 0
           rightspeed = 0
	   time.sleep(3)
           #leftMotor.run(Adafruit_MotorHAT.RELEASE)
           #rightMotor.run(Adafruit_MotorHAT.RELEASE)
       else:
           leftspeed = ((leftspeed*0.004)-0.006)
           rightspeed = ((rightspeed*0.004)-0.006)
       #print "Leftspeed Position:",leftspeed
       #print "Rightspeed Position:",rightspeed
       #velocity.velocityPid(leftspeed,rightspeed)
       capture.truncate(0)
       #return rightspeed, leftspeed
