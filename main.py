import sys
sys.path.insert(0, 'states/ImageProcessing/')
sys.path.insert(0, 'vision_processing/')
sys.path.insert(0, 'features/')
sys.path.insert(0, 'pyqt-mqtt/')
from joblib import load
from threading import Thread
import trackingline
import velocity
import time
import pisvm
from picamera import PiCamera
from picamera.array import PiRGBArray
import Queue
import cv2
import RPi.GPIO as GPIO
import multiprocessing
import slidingwindow
import numpy
import p_mqtt

from pi_video_stream import PiCamVideoStream

def runCamera(d,flag,slider, twofeed, messagetext, direction, GUIflag):
        vs = PiCamVideoStream().start()
        time.sleep(2.0)
        while(1):
            d['image'] = vs.read()
            raw.truncate(0)

def runRoadTracking(q, flag,slider, twofeed, messagetext, direction, GUIflag):
    velocity.leftSensorCallback(4)
    velocity.rightSensorCallback(17)
    velocity.getEncoderTicks()
    time.sleep(1)
    jobs = []
    cameraFunctions = [trackingline.position_p]
    functions = [velocity.getVelocity, velocity.velocityPid]

    for func in cameraFunctions:
        p = Thread(target=func, args=(q,flag,slider, twofeed, direction, GUIflag))
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

def paho(d, flag, slider, twofeed, messagetext, direction, GUIflag):
    p_mqtt.paho_client(d, flag, slider, twofeed, messagetext, direction, GUIflag)

def main():
    #init sensors
    slider = multiprocessing.Value('i', 0)
    twofeed = multiprocessing.Queue()
    messagetext = multiprocessing.Queue()
    direction = multiprocessing.Queue()

    manager = multiprocessing.Manager()
    d = manager.dict()
    d['image'] = numpy.zeros((480,640,3),numpy.uint8)
    flag = multiprocessing.Value('i', 0)
    GUIflag = multiprocessing.Value('i', 0)
    print "starting up..."

    jobs = []
    cameraFunctions = [runCamera]
    cameraFunctions.append(detect_stop_sign.process)
    cameraFunctions.append(runRoadTracking)
    cameraFunctions.append(paho)
    for func in cameraFunctions:
        p = multiprocessing.Process(target=func, args=(d,flag,slider, twofeed, messagetext, direction, GUIflag))
        jobs.append(p)
        p.daemon = True
        p.start()
        print "started {}, {}".format(func, p.pid)

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print "\nexiting..."
        GPIO.cleanup()
        velocity.stopMotors()
        cv2.destroyAllWindows()

if __name__=="__main__":
    main()
