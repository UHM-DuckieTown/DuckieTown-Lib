import RPi.GPIO as GPIO
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

mh = Adafruit_MotorHAT(addr=0x60)
leftMotor = mh.getMotor(2)
rightMotor = mh.getMotor(1)
leftMotor.run(Adafruit_MotorHAT.FORWARD)
rightMotor.run(Adafruit_MotorHAT.FORWARD)

def main():
    try:
        while True:
            print "Running"
            leftMotor.setSpeed(100)
            rightMotor.setSpeed(100)
            time.sleep(1)
    except KeyboardInterrupt:
        leftMotor.run(Adafruit_MotorHAT.RELEASE)
        rightMotor.run(Adafruit_MotorHAT.RELEASE)

if __name__=="__main__":
    main()
