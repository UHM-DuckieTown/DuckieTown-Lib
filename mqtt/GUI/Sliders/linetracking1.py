import numpy as np
import cv2
import base64
from picamera import PiCamera
import time
import paho.mqtt.client as mqtt
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from picamera.array import PiRGBArray
#cap = cv2.VideoCapture('silent.mp4')
#cap = cv2.VideoCapture('Video.MOV')
#cap = cv2.VideoCapture('duckie_vid.mp4')
#raw = cv2.imread('screen-shot.png');

MQTT_SERVER = "192.168.0.100"

DUCK1_FEED = "duck1_feed1"
DUCK1_FEED2 = "duck1_feed2"
DUCK1_TEXT = "duck1_text"

DUCK2_FEED = "duck2_feed"
DUCK2_FEED2 = "duck2_feed2"
DUCK2_TEXT = "duck2_text"

global command1
command = "0"
global command2
command2 = "5"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe([(DUCK1_TEXT,0),(DUCK2_TEXT,0)])

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    global command
    global command2
    #print (msg.topic+" "+str(msg.payload))
    if int(msg.payload) <= 4:
        command = msg.payload
    if int(msg.payload) >= 5:
        command2 = msg.payload
    print str(msg.payload)
    print'command' + ' '  + command
    print'command2' + ' '  + command2

def encode_string(image, topic, client):
    img_str = cv2.imencode('.jpg', image)[1].tostring()
    encoded_str = base64.b64encode(img_str)

    if topic == DUCK1_FEED:
        client.publish(DUCK1_FEED, encoded_str, 0)
    elif topic == DUCK2_FEED:
        client.publish(DUCK2_FEED, encoded_str, 0)
    elif topic == DUCK1_TEXT: 
        client.publish(DUCK1_FEED2, encoded_str, 0)
        #print 'test1'
    elif topic == DUCK2_TEXT:
        client.publish(DUCK2_FEED2, encoded_str, 0)
        #print 'test2'

    #print "In encode_string function"

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

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)
client.loop_start()

try:
    for frame in camera.capture_continuous(capture, format='bgr', use_video_port=True):
       #ret, raw = cap.read()
        image = capture.array
        raw = cv2.resize(image, (window_width, window_height))

#    rotate image
    #rows,cols,_ = raw.shape
    #rawrot = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    #raw = cv2.warpAffine(raw,rawrot,(cols,rows))


    #finished = cv2.resize(raw, (window_width, window_height))
#   ROI?
    #finished = finished[0:200,0:480]
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
        #cv2.imshow(" mask", mask)
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
        #print 'Average = ', avg

#cv2.imshow('frame', frame)
        #cv2.imshow('edges', edges)
#cv2.imshow('road', road)

#overlay = cv2.line(frame,(int(window_width/2),0),(int(window_width/2), int(window_height)),(0,0,255),5)
#cv2.imshow('overlay', overlay)

        encode_string(frame, DUCK1_FEED, client)
        #encode_string(frame, DUCK1_TEXT, client)
        encode_string(frame, DUCK2_FEED, client)

        #global render
        
        if command == "0":
            encode_string(raw, DUCK1_TEXT, client)
        elif command == "1":
            encode_string(edges, DUCK1_TEXT, client)
        elif command == "2":
            encode_string(frame, DUCK1_TEXT, client)
        elif command == "3":
            encode_string(mask1, DUCK1_TEXT, client)
        else:
            encode_string(mask2, DUCK1_TEXT, client)
            
        if command2 == "5":
            encode_string(raw, DUCK2_TEXT, client)
        elif command2 == "6":
            encode_string(edges, DUCK2_TEXT, client)
        elif command2 == "7":
            encode_string(frame, DUCK2_TEXT, client)
        elif command2 == "8":
            encode_string(mask1, DUCK2_TEXT, client)
        elif command2 == "9":
            encode_string(mask2, DUCK2_TEXT, client)
             

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    #global command

        if yellow:
            threshold = 105

        else:
            threshold = 430
        #130 for yellow line, 450 for white
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

        #print command
        if command == 'stop':
            leftMotor.run(Adafruit_MotorHAT.RELEASE)
            rightMotor.run(Adafruit_MotorHAT.RELEASE)

        else:
            leftMotor.run(Adafruit_MotorHAT.FORWARD)
            rightMotor.run(Adafruit_MotorHAT.FORWARD)
            rightMotor.setSpeed(rightspeed)
            leftMotor.setSpeed(leftspeed)

        rightMotor.setSpeed(rightspeed)
        leftMotor.setSpeed(leftspeed)
        #print 'Rightspeed = ',rightspeed
        capture.truncate(0)
except KeyboardInterrupt:
    leftMotor.run(Adafruit_MotorHAT.RELEASE)
    rightMotor.run(Adafruit_MotorHAT.RELEASE)

finally:
    client.loop_stop()
#cv2.destroyAllWindows()
