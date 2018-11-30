import time
import datetime
import RPi.GPIO as GPIO
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from threading import Thread
import matplotlib.pyplot as plt
import numpy as np
import trackingline

global leftencoderticks
leftencoderticks = 0
global lastleftencoderticks
lastleftencoderticks = 0
global rightencoderticks
rightencoderticks = 0
global lastrightencoderticks
lastrightencoderticks = 0

global left_vel
left_vel = 0
global right_vel
right_vel = 0

global L_errorP_v
L_errorP_v = 0
global L_old_errorP_v
L_old_errorP_v = 0
global L_errorD_v
L_errorD_v = 0
global L_errorI_v
L_errorI_v = 0
global L_totalError_v
L_totalError_v = 0


global R_errorP_v
R_errorP_v = 0
global R_old_errorP_v
R_old_errorP_v = 0
global R_errorD_v
R_errorD_v = 0
global R_errorI_v
R_errorI_v = 0
global R_totalError_v
R_totalError_v = 0

global target_left
target_left = []
global target_right
target_right = []

LEFTP = 3
LEFTI = 0.0001
LEFTD = 0.005
LEFTF = 0

RIGHTP = 3
RIGHTI = 0.0001
RIGHTD= 0.005
RIGHTF = 0

global left_velocity
left_velocity= []
global right_velocity
right_velocity = []
global samples
samples = []
global t
t = 0

global left_target
left_target = 0
global right_target
right_target = 0
# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)


mh = Adafruit_MotorHAT(addr=0x60)
leftMotor = mh.getMotor(2)
rightMotor = mh.getMotor(1)
leftMotor.run(Adafruit_MotorHAT.FORWARD)
rightMotor.run(Adafruit_MotorHAT.FORWARD)
def startMotors():
    leftMotor.run(Adafruit_MotorHAT.FORWARD)
    rightMotor.run(Adafruit_MotorHAT.FORWARD)
def stopMotors():
    leftMotor.run(Adafruit_MotorHAT.RELEASE)
    rightMotor.run(Adafruit_MotorHAT.RELEASE)

def leftSensorCallback(channel):
    global leftencoderticks
    leftencoderticks += 1
    #print "left encoder ticks:" + str(leftencoderticks)

def rightSensorCallback(channel):
    global rightencoderticks
    rightencoderticks += 1
    #print "right encoder ticks:" + str(rightencoderticks)


def plotVelocity():
    plt.figure(1, figsize=(5,4))
    plt.plot(samples, left_velocity)
    plt.plot(samples, target_left)
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


def velocityPid():
    waiting_for_thread = 0
    while True:
	if trackingline.stop == True:
	    if waiting_for_thread == 119:
		print "I entered that if statement"
	    	stopMotors()
		time.sleep(1)
	    	trackingline.stop = False
                startMotors()
		left_Motor.setSpeed(100)
		right_Motor.setSpeed(100)
		waiting_for_thread = 0
	    waiting_for_thread+=1
	global left_target
	global right_target
	if trackingline.stop == False:
	    #left_Motor.setSpeed(100)
	    #right_Motor.setSpeed(100)
 	    left_target = trackingline.leftspeed
	    right_target = trackingline.rightspeed
	#print "Left Target",left_target
	#print "Right Target",right_target
	#waiting_for_thread = 0
        global L_errorP_v
        L_errorP_v = left_target - left_vel
        global L_errorI_v
        L_errorI_v = L_errorI_v + L_errorP_v
        global L_errorD_v
        L_errorD_v = L_errorP_v - L_old_errorP_v
        global L_totalError_v
        L_totalError_v = LEFTP * L_errorP_v + LEFTI * L_errorI_v + LEFTD * L_errorD_v + LEFTF
        global L_old_errorP_v
        L_old_errorP_v = L_errorP_v

        #if left_target_vel > 0:
        #        if L_totalError_v > 1:
        #                global L_totalError_v
        #                L_totalError_v = 1
        #        elif L_totalError_v < 0:
        #                global L_totalError_v
        #                L_totalError_v = 0
        L_totalError_v = (L_totalError_v+0.006)/0.004
	if L_totalError_v > 255:
            speedL = 255
        elif L_totalError_v <0:
            speedL = 0
        else:
            speedL = int(L_totalError_v)
	#speedL = 100
        leftMotor.setSpeed(int(speedL))
        #print "Left Error Total: " + str(L_totalError_v)
        #print "Left Motor Speed: " + str(int(L_totalError_v + 100))
        #print "Left Cm/Sec: " + str(left_vel)


        global R_errorP_v
        R_errorP_v = right_target - right_vel
        global R_errorI_v
        R_errorI_v = R_errorI_v + R_errorP_v
        global R_errorD_v
        R_errorD_v = R_errorP_v - R_old_errorP_v
        global R_totalError_v
        R_totalError_v = RIGHTP * R_errorP_v + RIGHTI * R_errorI_v + RIGHTD * R_errorD_v + RIGHTF
        global R_old_errorP_v
        R_old_errorP_v = R_errorP_v

        #if right_target_vel > 0:
        #        if R_totalError_v > 1:
        #                global R_totalError_v
        #                R_totalError_v = 1
        #        elif R_totalError_v < 0:
        #                global R_totalError_v
        #                R_totalError_v = 0
	R_totalError_v = (R_totalError_v+0.006)/0.004
        if R_totalError_v > 255:
            speedR = 255
        elif R_totalError_v <0:
            speedR = 0
        else:
            speedR = int(R_totalError_v)
	#speedR = 100
        rightMotor.setSpeed(int(speedR))
        #print "Right Error Total: " + str(R_totalError_v)
        #print "Right Motor Speed: " + str(int(speedR))
        #print "Right Cm/Sec: " + str(right_vel)


        '''
        if len(samples) <= 5000:
            global left_velocity
            global right_velocity
            global samples
            global t
            global target_left
            global target_right
            left_velocity.append(left_vel)
            right_velocity.append(right_vel)
            t += 0.001
            samples.append(t)
            target_left.append(left_target_vel)
            target_right.append(right_target_vel)

        '''
        time.sleep(0.001)

def getEncoderTicks():
        # Set Switch GPIO as input
        # Pull high by default
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.BOTH, callback=leftSensorCallback)
        GPIO.add_event_detect(4, GPIO.BOTH, callback=rightSensorCallback)


'''
def main():
        leftSensorCallback(4)
	rightSensorCallback(17)

        threads = []
        encoder_polling = Thread(target = getVelocity)
        vel_pid = Thread(target = velocityPid)

        encoder_polling.setDaemon(True)
        vel_pid.setDaemon(True)

        threads.append(encoder_polling)
        threads.append(vel_pid)

        encoder_polling.start()
        vel_pid.start()

        #Max Speed: About 1.6 cm/s
        global left_target_vel
        left_target_vel = 0.3
        global right_target_vel
        right_target_vel = 0.3

        try:
                while True:
                        #print "looping"
                        time.sleep(1)
        except KeyboardInterrupt:
                print "done"
                leftMotor.run(Adafruit_MotorHAT.RELEASE)
                rightMotor.run(Adafruit_MotorHAT.RELEASE)
	        GPIO.cleanup()
		plotVelocity()


if __name__=="__main__":
        main()
'''
