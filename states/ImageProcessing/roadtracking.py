import time
import cv2
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import velocity
from threading import Thread
import RPi.GPIO as GPIO
import trackingline

#initialize encoders
velocity.getEncoderTicks()

time.sleep(0.1)




def main():


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
