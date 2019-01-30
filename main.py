from threading import Thread
import time


global Detect
Detect = 'a'

def threadOne():
    for i in range(20):
        print 'thread1 : {}'.format(Detect)
        if Detect == 'b':
            Detect = 'a'
def threadTwo():
    for i in range(20):
        print 'thread1 : {}'.format(Detect)
        global Detect

        if Detect == 'a':
            global Detect
            Detect = 'b'



def main():
        #init thread array
        functions = [threadOne, threadTwo]
        
        
        threads = []
        
        for proc in functions:
            process = Thread(target = proc)
            process.setDaemon(True)
            threads.append(process)
            process.start()

        for process in threads:
            process.join()

       

if __name__=="__main__":
        main()
