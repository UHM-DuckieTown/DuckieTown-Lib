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
#global L_errorP_v
#L_errorP_v = 0
global L_old_errorP_v
L_old_errorP_v = 0
#global L_errorD_v
#L_errorD_v = 0
global L_errorI_v
L_errorI_v = 0
#global L_totalError_v
#L_totalError_v = 0


#global R_errorP_v
#R_errorP_v = 0
global R_old_errorP_v
R_old_errorP_v = 0
#global R_errorD_v
#R_errorD_v = 0
global R_errorI_v
R_errorI_v = 0
#global R_totalError_v
#R_totalError_v = 0

global left_target
left_target = 0
global right_target
right_target = 0

#initialize values for pid constants
LEFTP = 3
LEFTI = 0.0001
LEFTD = 0.005
LEFTF = 0

RIGHTP = 3
RIGHTI = 0.0001
RIGHTD= 0.005
RIGHTF = 0

#initialize global variables used for plotting debug
global left_velocity
left_velocity= []
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

    #if stop line was found
	#if trackingline.stop == True:
    #    	global state
        #waits for 100 iterations of the thread before stopping the motors for the stop sign
	    #if waiting_for_thread == 100:
		#print "I entered that if statement"
	    #	stopMotors()
        #stops motors for 1 second
		#time.sleep(1)

	'''
		global rightencoderticks
        	currentencoderticks = rightencoderticks
        	if(rightencoderticks - currentencoderticks == 1152):
            		trackingline.stop = False
            		state = STOP
            		decision = randomn.randint(1,4)
            		if decision == 1:
                		state = RIGHTTURN
            		elif decision == 2:
                		state = LEFTTURN
            		elif decision == 3:
                		state = STRAIGHT
            		else:
                		state = POSITIONCONTROLLER
'''

                #startMotors()
		#left_Motor.setSpeed(100)
		#right_Motor.setSpeed(100)
		#waiting_for_thread = 0
	    #waiting_for_thread+=1

        #when no stop line is detected, resume normal operation
        #set targets equal to the speed given through position controller
        setMotorSpeed(1)
        setMotorSpeed(0)
	'''
            global left_target
            global right_target
            left_target = trackingline.leftspeed
            right_target = trackingline.rightspeed


        #calculate error for each pid controller constant
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


        #convert based on linear equation back to a motor speed value to
        #be fed into the motor hat function to set motor speed
        L_totalError_v = (L_totalError_v+0.006)/0.004
	if L_totalError_v > 255:
            speedL = 255
        elif L_totalError_v <0:
            speedL = 0
        else:
            speedL = int(L_totalError_v)
        leftMotor.setSpeed(int(speedL))

        #PID calculations
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

	R_totalError_v = (R_totalError_v+0.006)/0.004
        if R_totalError_v > 255:
            speedR = 255
        elif R_totalError_v <0:
            speedR = 0
        else:
            speedR = int(R_totalError_v)
        rightMotor.setSpeed(int(speedR))

'''


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
