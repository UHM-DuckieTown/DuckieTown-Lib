import paho.mqtt.client as mqtt
import numpy as np
import cv2
import base64

MQTT_SERVER = "168.105.238.127"
MQTT_PATH2 = "video_channel2"
MQTT_PATH4 = "text_channel2"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH3)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_start()
    try:
        camera = cv2.VideoCapture(0)

        while True:
            ret, image = camera.read()

            img_str = cv2.imencode('.jpg', image)[1].tostring()
            encoded_str = base64.b64encode(img_str)
            client.publish(MQTT_PATH2, encoded_str, 0)
            #print "Sent" + encoded_str


            #if cv2.waitKey(1) & 0xFF is ord('q'):
            #    break
    finally:
        client.loop_stop()

if __name__ == '__main__':
    main()
