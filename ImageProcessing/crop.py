import numpy as np
import cv2

cap = cv2.VideoCapture(0)
window_width = 320
window_height = 180

while(True):
    ret, raw = cap.read()
    raw = cv2.resize(raw, (window_width,window_height))
    #cv2.imshow('raw', raw)
    
    #overlay = cv2.line(raw,(int(window_width/2),0),(int(window_width/2), int(window_height)),(0,0,255),5)
    #cv2.imshow('overlay', overlay)
    road = raw[120 : 180, 0 : 320]
    
    
    frame_to_thresh = cv2.cvtColor(road, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(frame_to_thresh, (47, 108, 125), (119, 173, 255))
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
            cv2.circle(raw, (int(x), int(y)), int(radius),(255, 0, 0), 5)
            cv2.circle(raw, center, 3, (0, 0, 255), -1)
            cv2.putText(raw,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 0, 255),1)
            cv2.putText(raw,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 0, 255),1)


    """
    gray = cv2.cvtColor(road, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('gray', gray)
    _, contours, h = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print "Number of shapes: " + str(len(contours))
    for cnt in contours:
        #print('cnt',cnt)
        approx = cv2.approxPolyDP(cnt, 0.04*cv2.arcLength(cnt, True), True)
        cv2.drawContours(raw, [cnt], -1, (0, 255, 0), 2,offset = (0,120))
    """
    cv2.imshow('finished', raw)
    
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()