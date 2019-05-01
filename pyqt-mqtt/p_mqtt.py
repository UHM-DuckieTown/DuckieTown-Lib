import paho.mqtt.client as mqtt
import cv2
import base64
import numpy as np
import socket
import config
import Queue

l = Queue.Queue()
l.put("0")

p = Queue.Queue()

d1 = Queue.Queue()

def on_message_slider(client, userdata, msg):
    global duck_slider_val
    #Assign duck slider value based on received message topic
    # Receives value of the sliders as a text string
    duck_slider_val = msg.payload
    l.put(duck_slider_val)
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

    if duck_text[:2] == 'D:':
        if duck_text[3] == 'l' or duck_text[3] == "L":
            d1.put("left")
        if duck_text[3] == 'r' or duck_text[3] == "R":
            d1.put("right")
        if duck_text[3] == 's' or duck_text[3] == "S":
            d1.put("straight")

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
    #print "encoding"
    #print topic
    #Sends image string to topic specified
    client.publish(topic, encoded_str, 0)

def paho_client(d, flag, slider,twofeed, messagetext, direction, GUIflag):
    MQTT_SERVER = "192.168.0.100" #IP Address of Base Station

    print config.duck1_feed1
    print config.duck1_feed2
    print config.duck1_text

    DUCK1_FEED1 = config.duck1_feed1
    DUCK1_FEED2 = config.duck1_feed2
    DUCK1_TEXT = config.duck1_text
    DUCK1_SLIDER = config.duck1_slider

    # Create a client instance
    client = mqtt.Client()
    client.on_connect = on_connect
    #Connects the client to a broker
    client.on_message_slider = on_message_slider
    client.on_message_text = on_message_text
    client.connect(MQTT_SERVER, 1883, 60)
    #Runs a thread in the background to cal loop() automatically
    #Frees up main thread for other work
    client.loop_start()

    try:
        while(1):
            image = d["image"]
            #print "Got Next Image"
            if l.qsize() != 0:
                    slider.value = int(l.get())
            if p.qsize() != 0:
                    messagetext.put(p.get())
            if d1.qsize() != 0:
                    direction.put(d1.get())
            #print "Slider queue size: "+ str(slider.qsize())
            #print "SecondFeed queue size: "+ str(twofeed.qsize())
            #print "Textfeed queue size: "+ str(messagetext.qsize())
            encode_string(image,DUCK1_FEED1,client)
            encode_string(twofeed.get(),DUCK1_FEED2,client)
    finally:
        print("pau")
        client.loop_stop()
