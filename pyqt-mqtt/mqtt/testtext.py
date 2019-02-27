import paho.mqtt.publish as publish

MQTT_SERVER = "168.105.252.131"
MQTT_PATH = "test_channel"

test = " "
print "Enter String you want to send:"

while test != "q":
    test = raw_input()
    if test != "q":
        test = 'Publisher: ' + test
        publish.single(MQTT_PATH, test, hostname=MQTT_SERVER)
