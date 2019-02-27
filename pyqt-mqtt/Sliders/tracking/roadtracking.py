import time
import cv2
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import velocity
from threading import Thread
import RPi.GPIO as GPIO
import trackingline

#Added
import paho.mqtt.client as mqtt
import socket


#initialize encoders
velocity.getEncoderTicks()

time.sleep(0.1)

def main():

        MQTT_SERVER = "192.168.0.109" #IP Address of Base Station

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

        velocity.leftSensorCallback(4)
        velocity.rightSensorCallback(17)

        #debug prints
            #left_target_vel = 0.3
            #right_target_vel = 0.3
            #left_target_vel = ((trackingline.leftspeed*0.004) - 0.006)
            #right_target_vel = ((trackingline.rightspeed*0.004) - 0.006)
            #print "Position Left Vel:",left_target_vel
    	    #print "Position Right Vel:",right_target_vel

        #intialize empty list for threads
        threads = []

        #initialize threads
        position_adjust = Thread(target = trackingline.position_p)
        #position_adjust = Thread(target = trackingline.right_turn)
        encoder_polling = Thread(target = velocity.getVelocity)
        vel_pid = Thread(target = velocity.velocityPid)

        #initalize threads as a daemon thread
        #these threads are automatically terminated when the normal threads are terminated
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
                        time.sleep(0.1)
                        #print "looping"

        except KeyboardInterrupt:
                print "done"
                GPIO.cleanup()
                velocity.stopMotors()
                cv2.destroyAllWindows()
                #leftMotor.run(Adafruit_MotorHAT.RELEASE)
                #rightMotor.run(Adafruit_MotorHAT.RELEASE)


if __name__=="__main__":
        main()
