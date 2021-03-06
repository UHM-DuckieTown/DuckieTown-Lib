import cv2

from filter import FilterPipeline
from classifier import Classifier

def crop_contour(contour, frame):
    x,y,w,h = cv2.boundingRect(contour)
    y_top = max(0, y)
    y_bot = min(480, y+h)
    x_left = min(640, x+w)
    x_right = max(0, x)
    return frame[y_top:y_bot, x_right:x_left, :]

def process(d, flag, slider, twofeed, messagetext, direction):
    fp = FilterPipeline()
    clf = Classifier()
    img_counter = 1
    filename = "neg"
    while True:
        image = d['raw']
        image = image[70:190, :, :]
        img_name = "{}_{}.png".format(filename, img_counter)
        cv2.imwrite(img_name, image)
        print("{} written!".format(img_name))
        img_counter += 1
        '''
        #contours = fp.process(image)
        #for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            y_top = max(0, y)
            y_bot = min(480, y+h)
            x_left = min(640, x+w)
            x_right = max(0, x)
            clone = image.copy()
            cv2.rectangle(clone, (x_right,y_top), (x_left,y_bot), (255,0,0), 2)
            cropped = image[y_top:y_bot, x_right:x_left, :]

         #  contour = crop_contour(c, image)
         #  is_detected, pos_conf = clf.detect_stop_sign(contour)
            if is_detected and not flag.value:
                flag.value = 1
                cv2.imshow("bounding box on frame", clone)
                cv2.waitKey(1)
            cv2.imshow("display frame", image)
            cv2.waitKey(1)
            '''
