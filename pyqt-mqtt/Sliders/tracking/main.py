import sys
sys.path.insert(0, '../../states/ImageProcessing/')
sys.path.insert(0, '../../features/')
from joblib import load
from picamera import PiCamera
from threading import Thread
import trackingline2
import velocity2
import time
import pisvm
from picamera.array import PiRGBArray
import Queue
import cv2
import RPi.GPIO as GPIO
import multiprocessing

#Imports for MQTT
#import socket
import paho.mqtt.client as mqtt
import config
import p_mqtt


def runCamera(q):
        #camera config
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.framerate = 20
        raw = PiRGBArray(camera, size=(640,480))
        #camera warm up
        time.sleep(0.1)

        for _ in camera.capture_continuous(raw, format='bgr', use_video_port = True):
                q.put(raw.array)
                raw.truncate(0)

def runRoadTracking(q):
        velocity2.leftSensorCallback(4)
        velocity2.rightSensorCallback(17)
        velocity2.getEncoderTicks()
        time.sleep(0.1)
        print "starting up..."
        jobs = []
        cameraFunctions = [trackingline2.position_p]
        functions = [velocity2.getVelocity, velocity2.velocityPid]
        print "after camera function"

        for func in cameraFunctions:
            p = Thread(target=func, args=(q))
            jobs.append(p)
            p.daemon = True
            p.start()
            print "started {}".format(func)

        for func in functions:
            p = Thread(target=func)
            jobs.append(p)
            p.daemon = True
            p.start()
            print "started {}".format(func)

        for job in jobs:
                job.join()


def main():
        #init sensors

        q = multiprocessing.Queue()

        print "starting up..."
        jobs = []
##        cameraFunctions = [runCamera,pisvm.stopSignDetect]
        cameraFunctions = [runCamera]
        #functions = [velocity.getVelocity, velocity.velocityPid]

        for func in cameraFunctions:
            p = multiprocessing.Process(target=func, args=(q,))
            jobs.append(p)
            p.daemon = True
            p.start()
            print "started {}, {}".format(func, p.pid)

        p = multiprocessing.Process(target=runRoadTracking, args=(q))
        jobs.append(p)
        p.daemon = True
        p.start()
        print "started {}, {}".format(p, p.pid)


        try:
                while True:
                        time.sleep(1)
        except KeyboardInterrupt:
                print "\nexiting..."
                GPIO.cleanup()
                velocity2.stopMotors()
                cv2.destroyAllWindows()
        finally:
            client.loop_stop()

if __name__=="__main__":
        main()
