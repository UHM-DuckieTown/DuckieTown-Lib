import time
import RPi.GPIO as GPIO
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import matplotlib.pyplot as plt
import trackingline

#initialize global variables to count encoder ticks
global leftencoderticks
leftencoderticks = 0
global lastleftencoderticks
lastleftencoderticks = 0
global rightencoderticks
rightencoderticks = 0
global lastrightencoderticks
lastrightencoderticks = 0

#initialize global variables for setting velocity
global left_vel
left_vel = 0
global right_vel
right_vel = 0

#initialize global variables for pid controllers
global L_old_errorP_v
L_old_errorP_v = 0
global L_errorI_v
L_errorI_v = 0
global R_old_errorP_v
R_old_errorP_v = 0
global R_errorI_v
R_errorI_v = 0

global left_target
left_target = 0
global right_target
right_target = 0

#initialize global variables used for plotting debug
global left_velocity
left_velocity = []
global right_velocity
right_velocity = []
global samples
samples = []
global t
t = 0
global target_left
target_left = []
global target_right
target_right = []

# MACRO values for pid constants
LEFTP = 3
LEFTI = 0.0001
LEFTD = 0.005
LEFTF = 0

RIGHTP = 3
RIGHTI = 0.0001
RIGHTD= 0.005
RIGHTF = 0

# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)

#initialize motor hat/motors
mh = Adafruit_MotorHAT(addr=0x60)
leftMotor = mh.getMotor(2)
rightMotor = mh.getMotor(1)

#set motor direction
leftMotor.run(Adafruit_MotorHAT.FORWARD)
rightMotor.run(Adafruit_MotorHAT.FORWARD)

#function to set motors forward
def startMotors():
    leftMotor.run(Adafruit_MotorHAT.FORWARD)
    rightMotor.run(Adafruit_MotorHAT.FORWARD)

#function to stop motors
def stopMotors():
    leftMotor.run(Adafruit_MotorHAT.RELEASE)
    rightMotor.run(Adafruit_MotorHAT.RELEASE)

#functiosn feed into event detect in main
#iterates the encoder ticks by 1
def leftSensorCallback(channel):
    global leftencoderticks
    leftencoderticks += 1
    #print "left encoder ticks:" + str(leftencoderticks)

def rightSensorCallback(channel):
    global rightencoderticks
    rightencoderticks += 1
    #print "right encoder ticks:" + str(rightencoderticks)
def resetEncoders():
    global rightencoderticks
    global leftencoderticks
    rightencoderticks = 0
    leftencoderticks = 0
#uses matplotlib functions to plot velocity/targets
def plotVelocity():
    #generate new window to display the plots
    plt.figure(1, figsize=(5,4))

    #generate plot for velocity/time
    plt.plot(samples, left_velocity)
    #generate plot for target / time
    plt.plot(samples, target_left)
    #plot axis labels
    plt.xlabel('Time')
    plt.ylabel('Left Velocity')

    plt.figure(2, figsize=(5,4))
    plt.plot(samples, right_velocity)
    plt.plot(samples, target_right)
    plt.xlabel('Time')
    plt.ylabel('Right Velocity')
    plt.show()


def getVelocity():
        #Ticks per wheel rev: 384 ticks
        #Wheel Diam: 6.5 cm
        #Final constant: 0.053

        while True:
                #calculate ticks/sec and convert to cm/sec
                global left_vel
                left_vel = ((leftencoderticks - lastleftencoderticks) * 0.053)+0.005
                global lastleftencoderticks
                lastleftencoderticks = leftencoderticks

                global right_vel
                right_vel =((rightencoderticks - lastrightencoderticks) * 0.053)
                global lastrightencoderticks
                lastrightencoderticks = rightencoderticks

                #print "Left Cm/Sec: " + str(left_vel)
                #print "Right Cm/Sec: " + str(right_vel)
                time.sleep(0.01)

def setMotorSpeed(motor):
    global R_errorI_v
    global L_errorI_v
    global R_old_errorP_v
    global L_old_errorP_v

    if motor == 1:
        target = trackingline.rightspeed
        vel = right_vel
        errorI_v = R_errorI_v
        old_errorP_v = R_old_errorP_v
    else:
        target = trackingline.leftspeed
        vel = left_vel
        errorI_v = L_errorI_v
        old_errorP_v = L_old_errorP_v
        #PID calculations

    if target == 0:
        if motor == 1:
            rightMotor.setSpeed(0)
        else:
            leftMotor.setSpeed(0)
    else:
        errorP_v = target - vel
        errorI_v = errorI_v + errorP_v
        errorD_v = errorP_v - old_errorP_v
        totalError_v = RIGHTP * errorP_v + RIGHTI * errorI_v + RIGHTD * errorD_v + RIGHTF
        old_errorP_v = errorP_v

        totalError_v = (totalError_v+0.006)/0.004
        if totalError_v > 255:
            speed = 255
        elif totalError_v <0:
            speed = 0
        else:
            speed = int(totalError_v)
        if motor == 1:
            rightMotor.setSpeed(speed)
            R_old_errorP_v = old_errorP_v
            R_errorI_v = errorI_v
        else:
            leftMotor.setSpeed(speed)
            L_old_errorP_v = old_errorP_v
            L_errorI_v = errorI_v

#calculates error between current velocity and target velocity
#and adjusts motor speeds based on pid constants
def velocityPid():
    waiting_for_thread = 0
    L_errorI_v = 0
    R_errorI_v = 0
    while True:
        #when no stop line is detected, resume normal operation
        #set targets equal to the speed given through position controller
        setMotorSpeed(1)
        setMotorSpeed(0)
        time.sleep(0.001)

#function for thread to count encoder ticks
def getEncoderTicks():
        # Set Switch GPIO as input
        # Pull high by default
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #event detect occurs when change in signal is detected
        #set to detect both rising and falling edges of the signal
        #when triggered, runs functions left/rightSensorCallback which
        #iterate encoder ticks
        GPIO.add_event_detect(17, GPIO.BOTH, callback=leftSensorCallback)
        GPIO.add_event_detect(4, GPIO.BOTH, callback=rightSensorCallback)
