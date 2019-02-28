import sys
sys.path.insert(0, 'states/ImageProcessing/')
sys.path.insert(0, 'features/')
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
def main():

        #set threads that will be run
        #cameraFunctions = [pisvm.stopSignDetect,trackingline.position_p]
        cameraFunctions = []
        cameraFunctions.append(pisvm.stopSignDetect)
        #cameraFunctions.append(runCamera)
        #cameraFunctions.append(trackingline.position_p)
        
        #functions = [velocity.getVelocity, velocity.velocityPid]
        functions = []
        #functions.append(velocity.getVelocity)
        #functions.append(velocity.velocityPid)

        #init sensors
        velocity.leftSensorCallback(4)
        velocity.rightSensorCallback(17)
        velocity.getEncoderTicks()       
        q = Queue.Queue() 
        #init thread array
        threads = []
        print "starting up...." 
        for proc in cameraFunctions:
            print "{}".format(proc)
            process = Thread(target = proc, args=(q,))
            process.setDaemon(True)
            threads.append(process)
            process.start()
        for p in functions:
                process = Thread(target = p)
                process.setDaemon(True)
                threads.append(process)
                process.start()
        

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
