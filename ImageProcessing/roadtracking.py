import numpy as np
import cv2
import picamera as PiCamera
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from picamera.array import PiRGBArray
import velocity
from threading import Thread
import matplotlib.pyplot as plt
import datetime
import RPi.GPIO as GPIO
import trackingline

velocity.getEncoderTicks()
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
capture = PiRGBArray(camera, size=(640,480))
time.sleep(0.1)
'''
mh = Adafruit_MotorHAT(addr=0x60)
leftMotor = mh.getMotor(2)
rightMotor = mh.getMotor(1)
leftMotor.run(Adafruit_MotorHAT.FORWARD)
rightMotor.run(Adafruit_MotorHAT.FORWARD)
'''

'''
global leftencoderticks
leftencoderticks = 0

global lastleftencoderticks
lastleftencoderticks = 0

global rightencoderticks
rightencoderticks = 0

global lastrightencoderticks
lastrightencoderticks = 0



def leftSensorCallback(channel):
        global leftencoderticks
        leftencoderticks += 1
        print "left encoder ticks: " + str(leftencoderticks)

def rightSensorCallback(channel)
        global rightencoderticks
        rightencoderticks += 1
        print "right encoder ticks: " + str(rightencoderticks)
'''

def main():
        velocity.leftSensorCallback(4)
        velocity.rightSensorCallback(17)
        #left_target_vel = 0.3
        #right_target_vel = 0.3

        threads = []
        position_adjust = Thread(target = trackingline.position_p, args=(camera, capture))
        encoder_polling = Thread(target = velocity.getVelocity)
        vel_pid = Thread(target = velocity.velocityPid, args=(leftspeed, rightspeed))

        encoder_polling.setDaemon(True)
        vel_pid.setDaemon(True)
        position_adjust.setDaemon(True)

        threads.append(encoder_polling)
        threads.append(vel_pid)
        threads.append(position_adjust)

        encoder_polling.start()
        vel_pid.start()
        position_adjust.start()

        try:
                while True:
                        time.sleep(1)
                        print "looping"

        except KeyboardInterrupt:
                print "done"
                GPIO.cleanup()
                velocity.stopMotors()
                cv2.destroyAllWindows()
                #leftMotor.run(Adafruit_MotorHAT.RELEASE)
                #rightMotor.run(Adafruit_MotorHAT.RELEASE)


if __name__=="__main__":
        main()
