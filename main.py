import sys
sys.path.insert(0, 'features/')
from joblib import load
from picamera import PiCamera
from threading import Thread
import time
import pisvm
from picamera.array import PiRGBArray
import Queue
import cv2

image = []

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
        functions = [pisvm.stopSignDetect, runCamera]
        q = Queue.Queue() 
        #init thread array
        threads = []
        
        for proc in functions:
            process = Thread(target = proc, args=(q,))
            
            #allow child threads to exit
            process.setDaemon(True)
            threads.append(process)
            process.start()
        try:
                while True:
                        time.sleep(1)
        except KeyboardInterrupt:
                print "exiting..."

if __name__=="__main__":
        main()