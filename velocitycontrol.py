import time
import datetime
import RPi.GPIO as GPIO
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from threading import Thread

global leftencoderticks
leftencoderticks = 0
global lastleftencoderticks
lastleftencoderticks = 0
global rightencoderticks
rightencoderticks = 0
global lastrightencoderticks
lastrightencoderticks = 0

global left_target_vel
left_target_vel = 0
global left_vel
left_vel = 0
global right_target_vel
right_target_vel = 0
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


LEFTP = 1
LEFTI = 0
LEFTD = 0

RIGHTP = 1.1
RIGHTI = 0
RIGHTD= 0


# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)


mh = Adafruit_MotorHAT(addr=0x60)
leftMotor = mh.getMotor(1)
rightMotor = mh.getMotor(2)
leftMotor.run(Adafruit_MotorHAT.FORWARD)
rightMotor.run(Adafruit_MotorHAT.FORWARD)


def leftSensorCallback(channel):
        global leftencoderticks
        leftencoderticks += 1

def rightSensorCallback(channel):
        global rightencoderticks
        rightencoderticks += 1

def getVelocity():
        #Ticks per wheel rev: 384 ticks
        #Wheel Diam: 6.5 cm
        #Final constant: 0.053

        while True:
                global left_vel
                left_vel = (leftencoderticks - lastleftencoderticks) * 0.053
                global lastleftencoderticks
                lastleftencoderticks = leftencoderticks

                global right_vel
                right_vel = (rightencoderticks - lastrightencoderticks) * 0.053
                global lastrightencoderticks
                lastrightencoderticks = rightencoderticks
        
                #print "Left Cm/Sec: " + str(left_vel)
                #print "Right Cm/Sec: " + str(right_vel)

                time.sleep(0.01)

def velocityPid():
        while True:

                global L_errorP_v
                L_errorP_v = left_target_vel - left_vel
                global L_errorI_v
                L_errorI_v = L_errorI_v + L_errorP_v
                global L_errorD_v
                L_errorD_v = L_errorP_v - L_old_errorP_v
                global L_totalError_v
                L_totalError_v = LEFTP * L_errorP_v + LEFTI * L_errorI_v + LEFTD * L_errorD_v
                global L_old_errorP_v
                L_old_errorP_v = L_errorP_v

                if left_target_vel > 0:
                        if L_totalError_v > 1:
                                global L_totalError_v
                                L_totalError_v = 1
                        elif L_totalError_v < 0:
                                global L_totalError_v 
                                L_totalError_v = 0
                #leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                leftMotor.setSpeed(int(L_totalError_v * 200))
                print "Left Error P: " + str(L_errorP_v)

                global R_errorP_v
                R_errorP_v = right_target_vel - right_vel
                global R_errorI_v
                R_errorI_v = R_errorI_v + R_errorP_v
                global R_errorD_v
                R_errorD_v = R_errorP_v - R_old_errorP_v
                global R_totalError_v
                R_totalError_v = RIGHTP * R_errorP_v + RIGHTI * R_errorI_v + RIGHTD * R_errorD_v
                global R_old_errorP_v
                R_old_errorP_v = R_errorP_v

                if right_target_vel > 0:
                        if R_totalError_v > 1:
                                global R_totalError_v
                                R_totalError_v = 1
                        elif R_totalError_v < 0:
                                global R_totalError_v 
                                R_totalError_v = 0
                #rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                rightMotor.setSpeed(int(R_totalError_v * 200))
                print "Right Error P: " + str(R_errorP_v)
                time.sleep(0.01)


# Set Switch GPIO as input
# Pull high by default
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.BOTH, callback=leftSensorCallback)
GPIO.add_event_detect(4, GPIO.BOTH, callback=rightSensorCallback)



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
        
        global left_target_vel
        left_target_vel = 1
        global right_target_vel
        right_target_vel = 1
        
        try:
                while True:
                        #print "looping"
                        time.sleep(1)
        except KeyboardInterrupt:
                print "done"
                leftMotor.run(Adafruit_MotorHAT.RELEASE)
                rightMotor.run(Adafruit_MotorHAT.RELEASE)
	        GPIO.cleanup()


if __name__=="__main__":
        main()

