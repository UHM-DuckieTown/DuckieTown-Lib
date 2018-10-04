import time
import datetime
import RPi.GPIO as GPIO

def sensorCallback(channel):
    # Called if sensor output changes
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    if GPIO.input(channel):
        # No magnet
        print("Sensor HIGH " + stamp)
        else:
            # Magnet
            print("Sensor LOW " + stamp)

def main():
    # Wrap main content in a try block so we can
    # catch the user pressing CTRL-C and run the
    # GPIO cleanup function. This will also prevent
    # the user seeing lots of unnecessary error
    # messages.

    # Get initial reading
    sensorCallback(2)
        
        try:
            # Loop until users quits with CTRL-C
            while True :
                time.sleep(0.1)
                    except KeyboardInterrupt:
                        # Reset GPIO settings
                        GPIO.cleanup()

# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)

print("Setup GPIO pin as input on GPIO2")

# Set Switch GPIO as input
# Pull high by default
GPIO.setup(2 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(2, GPIO.BOTH, callback=sensorCallback, bouncetime=200)

if __name__=="__main__":
    main()

