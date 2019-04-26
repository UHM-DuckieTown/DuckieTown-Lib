import numpy as np
import cv2
from picamera import PiCamera
import time
import velocity
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from picamera.array import PiRGBArray
import random #remove this after states testing is done
#Global variables for the right and left speed of motor
global rightspeed
rightspeed = 0
global leftspeed
leftspeed = 0
#Global variable for camera object
#Set resolution and framerate of camera
#Images are read in as Numpy Arrays
#A sleep was recommended here to let the camera "warm up"
#Defining variables to hold proportional error in position,
#change in error in position and sum of error in position
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
#Flag to check if the Duck is stopped
#global stop
#stop = False
global image
#Kp, KD, and KI values
POSITIONP = 0.1
POSITIONI = 0.0000
POSITIOND = 0.1
POSITIONF = 0

global state
state = 1
#state macros
POSITIONCONTROLLER = 1
STOP = 2
RIGHTTURN = 3
LEFTTURN = 4
STRAIGHT = 5

RTURNRTICKS = 602
RTURNLTICKS = 1279
LTURNRTICKS = 1692
LTURNLTICKS = 1222
STRAIGHTTICKS = 1316


#This function takes in a frame that has already been converted
#into HSV and detects stop lines. If a stop line is found,
#the stop flag is set which stops the Duck.
def detect_stop(mask1, flag):
    global state
    stopsign = flag.value
    if stopsign:
        print "Flag is true"
    	#cv2.imshow('Stop Line Detection', mask1)
    	mask = mask1[0:280, 0:180];
    	#cv2.imshow('Stop Line Detection', mask)
    	#_,contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    	#Perform edge detection on the masked frame to find all edge points in image
    	edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    	#Use Hough Transform to find all lines in an image. The line of interest
    	#in this case is the stop line
    	lines = cv2.HoughLinesP(edges, 1, np.pi/180,10, minLineLength= 10, maxLineGap=1)
    	cv2.waitKey(20)
    	global stop
    	#for c in contours:
     	#   Moments = cv2.moments(c)
     	#  cX = int(Moments["m10"]/Moments["m00"])
     	#   cY = int(Moments["m01"]/Moments["m00"])
    	#For every line discovered by Hough Transform
        if lines is not None:
        	for line in lines:
                	x1, y1, x2, y2 = line[0]
                	cv2.line(mask, (x1, y1), (x2, y2), (0, 255, 0), 2)
                	cv2.circle(mask, (x1, y1),2,(255,0,0),3)
                	cv2.circle(mask,(x2,y2),2,(255,0,0),3)

            #Ignore the line if it leads to an undefined slope
	        #if (x2-x1) == 0:
	        #	continue
	        #else:
            	    #m = (y2-y1)/(x2-x1)

                #If the numerator of the slope is close enough to 0, the stop
                #line was found so anticipate stop
            	#if abs((y2-y1)/(x2-x1)) < 0.01:
        if np.all(cv2.bitwise_not(mask)) == False:
                #if cY < 150:
                 #if y2 < 350:
        	global state
                state = STOP
                 #else:
                    #print "stop line too far"

                    #stop = True
		    #print "Stop = ",stop
            #Exit Function once a stop is found
        flag.value = 0
        return
#This function takes in the raw image from the camera and will
#detect either the yellow or white road lines in the image
def linetracking(raw, stopsign,slider, twofeed):

#UI
#    print "in linetracking"
#    cv2.imshow('raw',raw)

#    key = cv2.waitKey(1) & 0xFF

#Minimize the region of interest to just the lower half of image
    #because that is where the road lines are
    raw = raw[200:480,0:480]
    #Blur the image to reduce the prominance of any noise
    frame = cv2.GaussianBlur(raw, (5, 5), 0)
    #Initialization of variables that will be used to find the midpoint of road
    #line
    Sum = 0
    numx = 0
    avg = 0

    #Convert the color of the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #The threshold values for yellow since road line is yellow
    min_yellow = np.array([0, 64, 216])
    max_yellow = np.array([32, 255, 255])
    #The threshold values for white since the outer roadlines are white
    upper = np.array([0, 0, 255])
    lower = np.array([0, 0, 191])
    #Ignore all pixels that aren't white to obtain a picture of only
    #the road lines
    mask1 = cv2.inRange(hsv, lower, upper)
    #cv2.imshow("white mask", mask1)

    #Ignore all pixels that aren't yellow to obtain a picture of only
    #the yellow road lines
    mask2 = cv2.inRange(hsv, min_yellow, max_yellow)
    #mask3 = cv2.bitwise_or(mask2, mask1)
    #if the yellow road lines are in the frame, use the yellow mask
    if np.all(cv2.bitwise_not(mask2)) == False:
        mask = mask2
        yellow = True
    #Otherwise use the white mask and track off of white road lines
    else:
        mask = mask1
	yellow = False
#ui
#    cv2.imshow(" mask", mask)
    #AND the original frame with the mask to obtain a picture with only the
    #road lines in it and black pixels everywhere else
    masked_img = cv2.bitwise_and(hsv, hsv, mask=mask)
    #Split the color channel to obtain a grey scaled image
    H, S, V = cv2.split(masked_img)
    #Apply Canny edge detection to detect the edge points of the road lines
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    #Apply the Hough Transform to detect lines in the image based on
    #the edge points that were detected
    lines = cv2.HoughLinesP(edges, 1, np.pi/180,20, minLineLength= 10, maxLineGap=1)
    if lines is not None:
        #For every line that is detected
        for line in lines:
            #Draw the 2 endpoints and a line between them to see what lines
            #were detected
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (x1, y1),2,(255,0,0),3)
            cv2.circle(frame,(x2,y2),2,(255,0,0),3)
            #Increment the number of x-values found
            numx += 2
            #Sum up the x-values
            Sum = Sum + x1 + x2
    old_avg = avg
    #As long as the x-values were obtained, calculate the average position in
    #the x-direction. This will be what is used when trying to correct the position
    if numx is not 0:
        avg = Sum/numx
    else:
        avg = old_avg
    #Draw a point to show where the average x-value is
    cv2.circle(frame,(avg,300),2,(0,0,255),3)
    detect_stop(mask1, stopsign)
#    cv2.imshow('frame', frame)
#    cv2.imshow('edges', edges)
#    cv2.waitKey(20)
    #if cv2.waitKey(20) & 0xFF == ord('q'):
        #break
    global old_slider

    if not slider.empty():
        slider_val = slider.get()

        #raw
        if slider_val == "start":
            twofeed.put(raw)
            old_slider = "0"

        elif slider_val == "0":
            twofeed.put(frame)
            old_slider = slider_val

        #edges
        elif slider_val == "1":
            twofeed.put(edges)
            old_slider = slider_val

        #masked image
        elif slider_val == "2":
            twofeed.put(masked_img)
            old_slider = slider_val

        #white mask
        elif slider == "3":
            twofeed.put(mask1)
            old_slider = slider_val

        #yellow mask
        elif slider == "4":
            twofeed.put(mask2)
            old_slider = slider_val

    else:
        #print "queue is empty"
        #print "Olde Slider" + str(old_slider)
        if old_slider == "0":
            twofeed.put(frame);
        if old_slider == "1":
            twofeed.put(edges)
        if old_slider == "2":
            twofeed.put(masked_img);
        if old_slider == "3":
            twofeed.put(mask1);
        if old_slider == "4":
            twofeed.put(mask2);

    return yellow,avg


def position_controller(target, actual):
    #Calculate the error in the position
    global Position_errorP_v
    Position_errorP_v = target-actual
    #Sum up the errors in position
    global Position_errorI_v
    Position_errorI_v = Position_errorI_v + Position_errorP_v
    #Calculate the change in error
    global Position_errorD_v
    Position_errorD_v = Position_errorP_v - Position_old_errorP_v
    #Sum up all three to obtain the total error in position
    global Position_totalError_v
    Position_totalError_v = POSITIONP * Position_errorP_v + POSITIONI * Position_errorI_v + POSITIOND *Position_errorD_v + POSITIONF
    global Position_old_errorP_v
    Position_old_errorP_v = Position_errorP_v
    #If our total error is less than 5, no adjustment is made
    #print 'Error = ',Position_totalError_v
    if abs(Position_totalError_v) < 5:
        #do nothing
        return int(0)
    #Otherwise the position will have to be adjusted
    else:
        adjustment = Position_totalError_v
        return int(adjustment)

def right_turn():
    global rightspeed
    global leftspeed
    leftspeed = 0.44
    rightspeed = 0.3

def left_turn():
    global rightspeed
    global leftspeed
    leftspeed = 0.3
    rightspeed = 0.42

def go_straight():
    global rightspeed
    global leftspeed
    leftspeed = 0.4
    rightspeed = 0.4

def position_p(d, flag,slider, twofeed):
    window_width = 480
    window_height = 360
    global camera
    global capture
    global state

    while(1):

        if state == STOP:
           # go_straight()
            print "in state stop"
            #velocity.resetEncoders()
           # if(velocity.rightencoderticks >= 800):
            #    print "Encoder's reached the value"
            leftspeed = 0
            rightspeed = 0
            time.sleep(2)

            velocity.resetEncoders()

                #decision = random.randint(1,4)
            decision = 4
            if decision == 1:
                state = RIGHTTURN
                velocity.resetEncoders()
            elif decision == 2:
                state = LEFTTURN
                velocity.resetEncoders()
            elif decision == 3:
                state = STRAIGHT
                velocity.resetEncoders()
            else:
                state = POSITIONCONTROLLER
        elif state == RIGHTTURN:
            right_turn()
            print "in state rightturn"
            if(velocity.rightencoderticks >= RTURNRTICKS or velocity.leftencoderticks >= RTURNLTICKS):
                state = POSITIONCONTROLLER


        elif state == LEFTTURN:
            left_turn()
            print "in state leftturn"
            if(velocity.rightencoderticks >= LTURNRTICKS or velocity.leftencoderticks >= LTURNLTICKS):
                state = POSITIONCONTROLLER

        elif state == STRAIGHT:
            go_straight()
            print "in state straight"
            if(velocity.rightencoderticks >= STRAIGHTTICKS or velocity.leftencoderticks >= STRAIGHTTICKS):
                state = POSITIONCONTROLLER
        else:
            #for each frame that is taken from the camera
            #Just for Timing Purposes
            start = 0
            flag.value = 0
            while True:
                global image
	            #print time.time()-start
	            #start = time.time()
                image = d["image"]
                #print "Got Next Image"
                #resize the image to make processing more manageable
                raw = cv2.resize(image, (window_width, window_height))
                #Find either the yellow or white line and what the average position
                #of the Duck is

                #testing purpose, controls stop sign detection
                #flag.put(0)

                yellow,avg = linetracking(raw, flag, slider, twofeed)
                #130 for yellow line, 450 for white
                #If tracking off the yellow line this is the target position to use
                #print "in state positioncontrol"
                if yellow:
                    threshold = 5
                #If tracking off the white line use this target position instead
                else:
                    threshold = 475
                if state == STOP:
			        global rightspeed
			        global leftspeed
			        rightspeed = 0.5
			        leftspeed = 0.5
			        velocity.resetEncoders()
			        break
                else:
                    global rightspeed
                    global leftspeed
                    #increase the right motor's speed and decrease the left motor's speed
                    #depending on the error in the position to correct the Duck
                    rightspeed = int(100 + position_controller(threshold,avg))
                    leftspeed = int(100 - position_controller(threshold,avg))
                    #rightspeed = 100
                    #leftspeed = 100
                    #Cap the Right and Left Motor speeds so that they do not go
                    #above 255 or less than 0
                    if rightspeed > 255:
                        rightspeed = 255

                    if rightspeed < 0:
                        rightspeed = 0

                    if leftspeed > 255:
                        leftspeed = 255

                    if leftspeed < 0:
                        leftspeed = 0


            	    #leftspeed = ((leftspeed*0.004)-0.006)
            	    #rightspeed = ((rightspeed*0.004)-0.006)
                    #Convert the left and right motor speed from 0-255 to a speed in
                    #cm/s since the velocity controller only takes in speeds in this unit
                    leftspeed = ((leftspeed*0.004)-0.006)
                    rightspeed = ((rightspeed*0.004)-0.006)
