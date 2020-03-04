import sys
sys.path.insert(0, 'states/ImageProcessing/')
sys.path.insert(0, 'vision_processing/')
sys.path.insert(0, 'pyqt-mqtt/')
from joblib import load
from threading import Thread
import trackingline
import velocity
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import Queue
import cv2
import RPi.GPIO as GPIO
import multiprocessing
import detect_stop_sign
import numpy
import p_mqtt

from pi_video_stream import PiCamVideoStream

def runCamera(frame, drive_state, display_option, display_frame, messagetext, direction):
    camera = PiCamera()
    camera.resolution = (640,480)
    camera.framerate = 20
    raw = PiRGBArray(camera, size=(640,480))
    #camera warm up
    time.sleep(0.1)
    for _ in camera.capture_continuous(raw, format='bgr', use_video_port = True):
        cv2.imshow("raw", raw.array)
        cv2.waitKey(1)
        frame['raw'] = raw.array
        raw.truncate(0)
    '''
    vs = PiCamVideoStream().start()
    time.sleep(2.0)
    while(1):
        d['image'] = vs.read()
    '''

def runRoadTracking(frame, drive_state, display_option, display_frame, messagetext, direction):
    velocity.leftSensorCallback(4)
    velocity.rightSensorCallback(17)
    velocity.getEncoderTicks()
    time.sleep(1)
    jobs = []
    cameraFunctions = [trackingline.position_p]
    functions = [velocity.getVelocity, velocity.velocityPid]

    for func in cameraFunctions:
        p = Thread(target=func, args=(frame, drive_state, display_option, display_frame, direction))
        jobs.append(p)
        p.daemon = True
        p.start()

    for func in functions:
        p = Thread(target=func)
        jobs.append(p)
        p.daemon = True
        p.start()

    for job in jobs:
        job.join()

def paho(frame, drive_state, display_option, display_frame, messagetext, direction):
    p_mqtt.paho_client(frame, drive_state, display_option, display_frame, messagetext, direction)

def main():
    #init sensors
    display_option = multiprocessing.Value('i', 0)
    display_frame = multiprocessing.Queue()
    messagetext = multiprocessing.Queue()
    direction = multiprocessing.Queue()

    manager = multiprocessing.Manager()
    frame = manager.dict()
    frame['raw'] = numpy.zeros((480,640,3),numpy.uint8)
    drive_state = multiprocessing.Value('i', 0)
    print "starting up..."

    jobs = []
    cameraFunctions = [runCamera]
    cameraFunctions.append(detect_stop_sign.process)
    cameraFunctions.append(runRoadTracking)
    cameraFunctions.append(paho)
    for func in cameraFunctions:
        p = multiprocessing.Process(target=func, args=(frame, drive_state, display_option, display_frame, messagetext, direction))
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
