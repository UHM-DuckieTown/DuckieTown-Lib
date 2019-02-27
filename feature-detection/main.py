from threading import Thread
import time
from pisvm import *

global image

def main():
        clf = load("clf_grid_Stop")

        #set threads that will be run
        functions = [runCamera]
        
        #read in svm object from file

        #init thread array
        threads = []
        
        for proc in functions:
            process = Thread(target = proc)
            
            #allow child threads to exit
            process.setDaemon(True)
            threads.append(process)
            process.start()

        for process in threads:
            process.join()
        

if __name__=="__main__":
        main()
