import numpy as np
import cv2
import base64
from picamera import PiCamera
import time
import socket
import paho.mqtt.client as mqtt
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from picamera.array import PiRGBArray
#cap = cv2.VideoCapture('silent.mp4')
#cap = cv2.VideoCapture('Video.MOV')
#cap = cv2.VideoCapture('duckie_vid.mp4')
#raw = cv2.imread('screen-shot.png');

#--------------------------- PyQT ---------------------------#
MQTT_SERVER = "192.168.0.109" #IP Address of Base Station

#Published-Topics
#Main Feeds to show Line Tracker Image

# TODO: Get IP Address of the Duck
ip_duck = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_duck = s.getsockname()[0]


# TODO: String manipulations
DUCK1_FEED1 = ip_duck + "_feed1"

#Secondary Feeds to show Raw, Edges, Line Tracker Image, White, and Yellow Mask
# TODO: String manipulations
DUCK1_FEED2 = ip_duck + "_feed2"

#Subscribed-Topics
# TODO: String manipulations
DUCK1_TEXT = ip_duck + "_text"

print DUCK1_FEED1
print DUCK1_FEED2
print DUCK1_TEXT

#Images corresponding to slider value received
RAW = "0"
EDGES = "1"
FRAME = "2"
MASK1 = "3"

#Initialization of feed selector
global duck_slider_val
duck_slider_val = "0"

#Function: on_connect
# The callback for when the client receives a CONNACK response from the server.
# Subscribes the client to one or more topics
#----
# client: the client instance for this callback
# userdata: user data as set in Client()
# flags: response flags sent by the broker
# rc: connection result
#----
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe([(DUCK1_TEXT,0)])

#Function on_message
# The callback for when a PUBLISH message is received from the server.
# Assign slider values from receiving message topic
#----
# client: the client instance for this callback
# userdata: user data as set in Client()
# msg: instance of MQTTMessage
#      Contains: Topic, Payload, QOS, Retain
#----
def on_message(client, userdata, msg):
    global duck_slider_val
#Assign duck slider value based on received message topic
# Receives value of the sliders as a text string
    duck_slider_val = msg.payload

    #print str(msg.payload)
    print'duck_slider_val' + ' '  + duck_slider_val

#Function encode_string
#Encodes images to strings to be sent to given topics
#----
# image: OpenCV image
# topic: topic string to which the image will be published to
# client: the client instance for this callback
#----
def encode_string(image, topic, client):
    #Converts image to string
    img_str = cv2.imencode('.jpg', image)[1].tostring()
    #Converts string to only contain ascii values
    encoded_str = base64.b64encode(img_str)

    #Sends image string to topic specified
    client.publish(topic, encoded_str, 0)
#--------------------------- PyQT ---------------------------#

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

#--------------------------- PyQT ---------------------------#
# Create a client instance
client = mqtt.Client()
client.on_connect = on_connect
#Connects the client to a broker
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)
#Runs a thread in the background to cal loop() automatically
#Frees up main thread for other work
client.loop_start()
#--------------------------- PyQT ---------------------------#

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
#--------------------------- PyQT ---------------------------#
        #Calls encode_string to send given image to corresponding topic
        encode_string(frame, DUCK1_FEED1, client)

        #Dependent on duck1_slider_val
        #Calls encode_string to send given image to corresponding topic
        if duck_slider_val == RAW:
            encode_string(raw, DUCK1_FEED2, client)
        elif duck_slider_val == EDGES:
            encode_string(edges, DUCK1_FEED2, client)
        elif duck_slider_val == FRAME:
            encode_string(frame, DUCK1_FEED2, client)
        elif duck_slider_val == MASK1:
            encode_string(mask1, DUCK1_FEED2, client)
        else:
            encode_string(mask2, DUCK1_FEED2, client)

#--------------------------- PyQT ---------------------------#

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

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

        # if duck1_slider_val == 'stop':
        #     leftMotor.run(Adafruit_MotorHAT.RELEASE)
        #     rightMotor.run(Adafruit_MotorHAT.RELEASE)
        #
        # else:
        #     leftMotor.run(Adafruit_MotorHAT.FORWARD)
        #     rightMotor.run(Adafruit_MotorHAT.FORWARD)
        #     rightMotor.setSpeed(rightspeed)
        #     leftMotor.setSpeed(leftspeed)

        rightMotor.setSpeed(rightspeed)
        leftMotor.setSpeed(leftspeed)
        #print 'Rightspeed = ',rightspeed
        capture.truncate(0)
except KeyboardInterrupt:
    leftMotor.run(Adafruit_MotorHAT.RELEASE)
    rightMotor.run(Adafruit_MotorHAT.RELEASE)

finally:
    #Stop Background thread
    client.loop_stop()
#cv2.destroyAllWindows()
