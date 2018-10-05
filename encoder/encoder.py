# Import required libraries
import time
import datetime
import RPi.GPIO as GPIO

def leftSensorCallback(channel):
	# Called if sensor output changes
	
	global leftencoderticks

	if GPIO.input(channel):
        	# No magnet

    		#print("Sensor HIGH "+stamp )
		leftencoderticks += 1
		print leftencoderticks
    	else:
     	# Magnet

		#print("Sensor LOW "+stamp )
		leftencoderticks += 1
		print leftencoderticks

def rightSensorCallback(channel):
        # Called if sensor output changes
       
        global rightencoderticks

        if GPIO.input(channel):
                # No magnet

                #print("Sensor HIGH "+stamp )
                rightencoderticks += 1
                print rightencoderticks
        else:
        # Magnet

                #print("Sensor LOW "+stamp )
                rightencoderticks += 1
                print rightencoderticks

def main():
    # Wrap main content in a try block so we can
    # catch the user pressing CTRL-C and run the
    # GPIO cleanup function. This will also prevent
    # the user seeing lots of unnecessary error
    # messages.

	# Get initial reading
	leftSensorCallback(2)
	rightSensorCallback(4)

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

leftencoderticks = 0
rightencoderticks = 0
# Set Switch GPIO as input
# Pull high by default
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(2, GPIO.BOTH, callback=leftSensorCallback, bouncetime=1)
GPIO.add_event_detect(4, GPIO.BOTH, callback=rightSensorCallback, bouncetime=1)

if __name__=="__main__":
	main()


