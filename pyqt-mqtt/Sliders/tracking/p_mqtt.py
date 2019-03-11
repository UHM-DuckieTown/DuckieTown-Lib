import paho.mqtt.client as mqtt
import cv2
import base64
import numpy as np
import socket
import config
import Queue

q = Queue.Queue()
q.put("start")

p = Queue.Queue()

def on_message_slider(client, userdata, msg):
    global duck_slider_val
    #Assign duck slider value based on received message topic
    # Receives value of the sliders as a text string
    duck_slider_val = msg.payload
    q.put(duck_slider_val)
    #print q.qsize()
    #print str(msg.payload)
    print'duck_slider_val' + ' '  + duck_slider_val

def on_message_text(client, userdata, msg):
    global duck_text
    #Assign duck slider value based on received message topic
    # Receives value of the sliders as a text string
    duck_text = msg.payload
    p.put(duck_text)
    #print q.qsize()
    #print str(msg.payload)
    print 'In direction Queue' + ' '  + duck_text
    print 'Queue size: '+ str(p.qsize())

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    DUCK1_TEXT = config.duck1_text
    DUCK1_SLIDER = config.duck1_slider
    client.message_callback_add(DUCK1_TEXT, on_message_text)
    client.message_callback_add(DUCK1_SLIDER, on_message_slider)
    client.subscribe([(DUCK1_TEXT,0),(DUCK1_SLIDER,0)])
    #client.subscribe([('192.168.0.69_text',0)])

def encode_string(image, topic, client):
    #Converts image to string
    img_str = cv2.imencode('.jpg', image)[1].tostring()
    #Converts string to only contain ascii values
    encoded_str = base64.b64encode(img_str)

    #Sends image string to topic specified
    client.publish(topic, encoded_str, 0)
