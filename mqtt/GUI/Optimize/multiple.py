import cv2
import numpy as np
import paho.mqtt.client as mqtt
import base64
from matplotlib import pyplot as plt
import Queue as queue

MQTT_SERVER = "localhost"

DUCK1_FEED = "duckiefeed/duck1/feed1"
DUCK1_FEED2 = "duckiefeed/duck1/feed2"
DUCK1_TEXT = "duckietext/duck1/text"

DUCK2_FEED = "duckiefeed/duck2/feed1"
DUCK2_FEED2 = "duckiefeed/duck2/feed2"
DUCK2_TEXT = "duckietext/duck2/text"

img = cv2.imread('capture.png')
raw = cv2.imread('capture.png')

q = queue.Queue()

size = cv2.resize(raw, (800, 800))
blue = np.uint8([[[255, 0, 0]]])
hsv_blue = cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)
img = cv2.cvtColor(raw, cv2.COLOR_BGR2HSV)
lower = np.array([100, 100, 100])
higher = np.array([135, 255, 255])

mask = cv2.inRange(img, lower, higher)

res = cv2.bitwise_and(img, img, mask = mask)

H, S, V = cv2.split(res)
iterator = int(1)

blurry = cv2.GaussianBlur(V, (11, 11), 0)

ret, thresh = cv2.threshold(blurry, 120, 255, cv2.THRESH_BINARY)

_, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(contours)):
    contour = contours[i]
    epsilon = 0.01*cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    #Calculate Moments to find center of shapes in order to place text there
    Moment = cv2.moments(contour)

    if len(approx) == 3:
        print "Triangle"
        cX = int(Moment["m10"]/Moment["m00"])
        cY = int(Moment["m01"]/Moment["m00"])
        cv2.drawContours(img, [contour], -1, (255, 255, 255), 3)
        cv2.putText(raw, "Triangle", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
            1.5, (255, 255, 255), 4)

    elif len(approx) == 4:
        print "Rectangle"
        cX = int(Moment["m10"]/Moment["m00"])
        cY = int(Moment["m01"]/Moment["m00"])
        cv2.drawContours(raw, [contour], -1, (255, 255, 255), 3)
        cv2.putText(raw, "Rectangle", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
            1.5, (255, 255, 255), 4)

    elif len(approx) == 5:
        print "Pentagon"
        cX = int(Moment["m10"]/Moment["m00"])
        cY = int(Moment["m01"]/Moment["m00"])
        cv2.drawContours(raw, [contour], -1, (255, 255, 255), 3)
        cv2.putText(raw, "Pentagon", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
            1.5, (255, 255, 255), 4)

    elif len(approx) == 6:
        print "Hexagon"
        cX = int(Moment["m10"]/Moment["m00"])
        cY = int(Moment["m01"]/Moment["m00"])
        cv2.drawContours(raw, [contour], -1, (255, 255, 255), 3)
        cv2.putText(raw, "Hexagon", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
            1.5, (255, 255, 255), 4)

    elif len(approx) > 6:
        cX = int(Moment["m10"]/Moment["m00"])
        cY = int(Moment["m01"]/Moment["m00"])
        print "Circle", len(approx)
        cv2.drawContours(raw, [contour], -1, (255, 255, 255), 3)
        cv2.putText(raw, "Circle", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
        1.5, (255, 255, 255), 4)
    else:
        print "Mystery", len(approx)
    iterator += 1


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([(DUCK1_TEXT, 0), (DUCK2_TEXT, 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    print(msg.topic+" "+str(msg.payload))
    q.put((msg.payload, str(msg.topic)))

def encode_string(image, topic, client):
    img_str = cv2.imencode('.jpg', image)[1].tostring()
    encoded_str = base64.b64encode(img_str)

    if topic == DUCK1_FEED:
        client.publish(DUCK1_FEED, encoded_str, 0)
    elif topic == DUCK2_FEED:
        client.publish(DUCK2_FEED, encoded_str, 0)
    elif topic == DUCK1_TEXT:
        client.publish(DUCK1_FEED2, encoded_str, 0)
    elif topic == DUCK2_TEXT:
        client.publish(DUCK2_FEED2, encoded_str, 0)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_start()

    try:
        camera = cv2.VideoCapture(0)

        while True:

            encode_string(raw, DUCK1_FEED, client)
            encode_string(raw, DUCK2_FEED, client)

            if not q.empty():
                command, topic = q.get()

                if command == "0":
                    print 'none'

                elif command == "1":
                    render = res
                    print 'res'

                elif command == "2":
                    render = thresh
                    print 'thresh'

                elif command == "3":
                    render = raw
                    print 'raw'

                elif command == "4":
                    render = mask
                    print 'mask'

                elif command == "5":
                    print 'none'

                encode_string(render, topic, client)
                print "video"

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
