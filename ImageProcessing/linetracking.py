import numpy as np
import cv2
from picamera import PiCamera
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from picamera.array import PiRGBArray
import trackingline
#cap = cv2.VideoCapture('silent.mp4')
#cap = cv2.VideoCapture('Video.MOV')
#cap = cv2.VideoCapture('duckie_vid.mp4')
#raw = cv2.imread('screen-shot.png');
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
capture = PiRGBArray(camera, size=(640,480))
time.sleep(0.1)
#'''
 #   window_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
  #  window_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

#    print "Width: " + str(window_width)
 #   print "Height: " + str(window_height)
  #  '''

window_width = 480
window_height = 360
ROI_road_offset = int(0.66*window_height)
mh = Adafruit_MotorHAT(addr=0x60)
leftMotor = mh.getMotor(2)
rightMotor = mh.getMotor(1)
leftMotor.run(Adafruit_MotorHAT.FORWARD)
rightMotor.run(Adafruit_MotorHAT.FORWARD)
#global old_error
#old_error = 0
#rightMotor.setSpeed(int(255))
#leftMotor.setSpeed(int(255))
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
try:
    for frame in camera.capture_continuous(capture, format='bgr', use_video_port=True):
       #ret, raw = cap.read()
       image = capture.array
       raw = cv2.resize(image, (window_width, window_height))
       Kp = 0.15
       #    rotate image
           #rows,cols,_ = raw.shape
           #rawrot = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
           #raw = cv2.warpAffine(raw,rawrot,(cols,rows))


           #finished = cv2.resize(raw, (window_width, window_height))
       #   ROI?
           #finished = finished[0:200,0:480]
           '''
       	raw = raw[300:480,0:480]
               frame = cv2.GaussianBlur(raw, (5, 5), 0)
               Sum = 0
               numx = 0
               avg = 0
       	Kp = 0.15
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
       #cv2.imshow('road', road)

       #overlay = cv2.line(frame,(int(window_width/2),0),(int(window_width/2), int(window_height)),(0,0,255),5)
       #cv2.imshow('overlay', overlay)

               if cv2.waitKey(20) & 0xFF == ord('q'):
                   break
           '''

       yellow,avg = trackingline(raw)
       #130 for yellow line, 450 for white
       if yellow:
           threshold = 105

       else:
           threshold = 430

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

       rightMotor.setSpeed(rightspeed)
       leftMotor.setSpeed(leftspeed)
       print 'Rightspeed = ',rightspeed
       capture.truncate(0)
       
except KeyboardInterrupt:
	leftMotor.run(Adafruit_MotorHAT.RELEASE)
	rightMotor.run(Adafruit_MotorHAT.RELEASE)
cv2.destroyAllWindows()
