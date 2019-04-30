import sys
sys.path.insert(0, 'states/ImageProcessing/')
sys.path.insert(0, 'features/')
sys.path.insert(0, 'pyqt-mqtt/')
from joblib import load
from picamera import PiCamera
from threading import Thread
import trackingline
import velocity
import time
import pisvm
from picamera.array import PiRGBArray
import Queue
import cv2
import RPi.GPIO as GPIO
import multiprocessing
import slidingwindow
import numpy
import p_mqtt

def runCamera(d,flag,slider, twofeed, messagetext):
        #camera config
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.framerate = 20
        raw = PiRGBArray(camera, size=(640,480))
        #camera warm up
        time.sleep(0.1)
        for _ in camera.capture_continuous(raw, format='bgr', use_video_port = True):
            #cv2.imshow("live feed", raw.array)
            #cv2.waitKey(20)
            #if q.qsize() >= 10:
            #    q.get()
            d['image'] = raw.array
            raw.truncate(0)
            #print q.qsize()

def runRoadTracking(q, flag,slider, twofeed, messagetext, direction):
        velocity.leftSensorCallback(4)
        velocity.rightSensorCallback(17)
        velocity.getEncoderTicks()
        time.sleep(1)
        jobs = []
        cameraFunctions = [trackingline.position_p]
        functions = [velocity.getVelocity, velocity.velocityPid]

        for func in cameraFunctions:
            p = Thread(target=func, args=(q,flag,slider, twofeed))
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

def paho(d, flag, slider, twofeed, messagetext, direction):
        p_mqtt.paho_client(d, slider, twofeed, messagetext, direction)

def main():
        #init sensors
        #q = multiprocessing.Queue()
        slider = multiprocessing.Value('i', 0)
        twofeed = multiprocessing.Queue()
        messagetext = multiprocessing.Queue()
        direction = multiprocessing.Queue()
        #q = multiprocessing.Array('d', numpy.zeros((480,640,3),numpy.uint8))
        manager = multiprocessing.Manager()
        d = manager.dict()
        d['image'] = numpy.zeros((480,640,3),numpy.uint8)
        flag = multiprocessing.Value('i', 0)
        print "starting up..."
        jobs = []
        cameraFunctions = [runCamera]
        cameraFunctions.append(slidingwindow.img_proc)
        cameraFunctions.append(runRoadTracking)
        cameraFunctions.append(paho)
        for func in cameraFunctions:
            p = multiprocessing.Process(target=func, args=(d,flag,slider, twofeed, messagetext, direction))
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
