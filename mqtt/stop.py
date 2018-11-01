from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time

mh = Adafruit_MotorHAT(addr=0x60)
motor1 = mh.getMotor(1)
motor2 = mh.getMotor(2)

motor1.setSpeed(150)
motor2.setSpeed(150)

while (True):
	motor1.run(Adafruit_MotorHAT.RELEASE)
	motor2.run(Adafruit_MotorHAT.RELEASE)
	time.sleep(1)
