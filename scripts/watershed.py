import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

camera = PiCamera()
camera.resolution = (640,480)
raw = PiRGBArray(camera, size=(640, 480))


def display_roi(image, coordinates, window_size):
    mask = np.zeros(image.shape, dtype=np.uint8)
    x_offset = int((window_size[0] - 1) / 2)
    y_offset = int((window_size[1] - 1) / 2)

    for (x, y) in coordinates:
        x_min, x_max = x - x_offset, x + x_offset
        y_min, y_max = y - y_offset, y + y_offset
        mask[y_min:y_max, x_min:x_max] = 1
    
    display_img = np.zeros(image.shape, dtype=np.uint8)
    display_img[mask == 1] = image[mask == 1]
    return display_img

for frame in camera.capture_continuous(raw, format='bgr', use_video_port=True):
    image = raw.array
    cv2.imshow("raw",image)
    image = image[75:175,:] 
    cv2.imshow("cropped", image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Settings
    kernel = np.ones((9, 9), dtype=int)
    threshold = image.max() / 4

    tophat_image = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    ret, thresh = cv2.threshold(tophat_image, threshold, 255, cv2.THRESH_BINARY)

    
    # Watershed region growing algorithm with the spotlights as the seeds
    dist_transform = cv2.distanceTransform(np.uint8(thresh), cv2.DIST_L2, 5)
    ret, markers = cv2.connectedComponents(np.uint8(dist_transform))

    # Make sure the background is not 0
    markers += 1
    watershed_image = cv2.watershed(image, markers)

    max_size = 300

    # Grab the marker values and how many times they occur
    values, counts = np.unique(watershed_image, return_counts=True)

    # Get the indices of where the segments are under the max size
    segment_indices = np.where(counts <= max_size)
    markers = values[segment_indices]

    # Get the median coordinates of the markers (roughly the center)
    coordinates = []
    for marker in markers:
        y_coordinates, x_coordinates = np.where(watershed_image == marker)
        coordinates.append((int(np.median(x_coordinates)), int(np.median(y_coordinates))))
    print("Number of windows found: {}".format(len(coordinates)))
    cv2.imshow("roi", display_roi(image, coordinates, window_size=(32, 64)))
    cv2.waitKey(1)
    raw.truncate(0)

cam.release()
cv2.destroyAllWindows()
