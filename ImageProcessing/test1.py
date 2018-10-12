import numpy as np
import cv2
#cap = cv2.VideoCapture('silent.mp4')
cap = cv2.VideoCapture('Video.MOV')

'''
window_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
window_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print "Width: " + str(window_width)
print "Height: " + str(window_height)
'''

window_width = 480
window_height = 360
ROI_road_offset = int(0.66*window_height)

while(True):
    ret, raw = cap.read()
    #raw = cv2.resize(raw, (window_width, window_height))
    finished = cv2.resize(raw, (window_width, window_height))
    frame = cv2.GaussianBlur(finished, (5, 5), 0)

    #road = raw[ROI_road_offset:window_height, 0:window_width]

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    min_yellow = np.array([18, 94, 140])
    max_yellow = np.array([48, 255, 255])
    upper = np.array([0, 0, 255])
    lower = np.array([0, 0, 255])
    mask1 = cv2.inRange(hsv, lower, upper)
    #cv2.imshow("white mask", mask1)
    
    mask2 = cv2.inRange(hsv, min_yellow, max_yellow)
    mask = cv2.bitwise_or(mask2, mask1)
    masked_img = cv2.bitwise_and(hsv, hsv, mask=mask)
    H, S, V = cv2.split(masked_img)
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180,100, minLineLength= 50, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('frame', frame)
    cv2.imshow('edges', edges)
    #cv2.imshow('road', road)

    #overlay = cv2.line(frame,(int(window_width/2),0),(int(window_width/2), int(window_height)),(0,0,255),5)
    #cv2.imshow('overlay', overlay)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
