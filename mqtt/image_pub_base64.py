import paho.mqtt.publish as publish
import base64
import argparse
import numpy as np
import cv2
import time

MQTT_SERVER = "local_host"
MQTT_PATH = "test_channel"

def callback(value):
    pass


def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)


def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--filter', required=True,
                    help='Range filter. RGB or HSV')
    args = vars(ap.parse_args())

    if not args['filter'].upper() in ['RGB', 'HSV']:
        ap.error("Please speciy a correct filter.")

    return args


def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)
    return values

count = 0

def main():
    args = get_arguments()
    global count
    endtime = time.time() + 60

    range_filter = args['filter'].upper()

    camera = cv2.VideoCapture(0)

    setup_trackbars(range_filter)

    while True:
        ret, image = camera.read()

        if not ret:
            break

        if range_filter == 'RGB':
            frame_to_thresh = image.copy()
        else:
            frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)



        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # find contours
        # get center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # if a countour has been found
        if len(cnts) > 0:
            # find the largest contour
            # compute circle
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # if image is big enough
            if radius > 10:
                # draw the circle
                # update list
                cv2.circle(image, (int(x), int(y)), int(radius),(255, 0, 0), 5)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(image,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 0, 255),1)
                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 0, 255),1)

        # show the image
        #cv2.imshow("Original", image)
        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Mask", mask)

        if time.time() < endtime:
                count = count + 1
                print count

        img_str = cv2.imencode('.jpg', image)[1].tostring()
        encoded_str = base64.b64encode(img_str)
        publish.single(MQTT_PATH, encoded_str, 0)
        #print "Sent" + encoded_str


        if cv2.waitKey(1) & 0xFF is ord('q'):
            break

if __name__ == '__main__':
    main()
