import time
import datetime
import RPi.GPIO as GPIO
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import matplotlib.pyplot as plt
import numpy as np
import velocity
from threading import Thread

def main():
	GPIO.setmode(GPIO.BCM)
	mh = Adafruit_MotorHAT(addr=0x60)
	leftMotor = mh.getMotor(2)
	rightMotor = mh.getMotor(1)
	leftMotor.run(Adafruit_MotorHAT.BACKWARD)
	rightMotor.run(Adafruit_MotorHAT.FORWARD)
	speed = 0
	velocity.getEncoderTicks()
	velocity.left_target_vel = 0
	velocity.right_target_vel = 0
	velocity.t = 0
	velocity.leftSensorCallback(4)
	velocity.rightSensorCallback(17)
	threads = []
	encoder_polling = Thread(target = velocity.getVelocity)
	encoder_polling.setDaemon(True)
	threads.append(encoder_polling)
	encoder_polling.start()
	while True:
		#velocity.getEncoderTicks()
		#velocity.leftSensorCallback(4)
		#velocity.rightSensorCallback(17)
		#velocity.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
		#velocity.rightMotor.run(Adafruit_MotorHAT.FORWARD)
		leftMotor.setSpeed(speed)
		rightMotor.setSpeed(speed)
		#velocity.getVelocity()
		velocity.left_velocity.append(velocity.left_vel)
		velocity.right_velocity.append(velocity.right_vel)
		velocity.t+=1
		velocity.samples.append(velocity.t)
		velocity.target_left.append(velocity.left_target_vel)
		velocity.target_right.append(velocity.right_target_vel)
		time.sleep(1)
		speed +=1
		print "Speed",speed
		if speed > 255:
			break
	leftMotor.run(Adafruit_MotorHAT.RELEASE)
	rightMotor.run(Adafruit_MotorHAT.RELEASE)
	velocity.plotVelocity()
if __name__=="__main__":
	main()
