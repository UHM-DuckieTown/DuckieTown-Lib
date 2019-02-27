import paho.mqtt.client as mqtt
import cv2
import base64
import numpy as np

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #client.subscribe([(DUCK1_TEXT,0)])

def on_message(client, userdata, msg):
    global duck_slider_val
    #Assign duck slider value based on received message topic
    # Receives value of the sliders as a text string
    duck_slider_val = msg.payload
    #print str(msg.payload)
    print'duck_slider_val' + ' '  + duck_slider_val

def encode_string(image, topic, client):
    #Converts image to string
    img_str = cv2.imencode('.jpg', image)[1].tostring()
    #Converts string to only contain ascii values
    encoded_str = base64.b64encode(img_str)

    #Sends image string to topic specified
    client.publish(topic, encoded_str, 0)
