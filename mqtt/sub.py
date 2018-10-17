import paho.mqtt.client as mqtt
import numpy as np
import cv2
import base64
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

MQTT_SERVER = "2607:f278:410e:5:5d0d:af35:dd83:7058"
MQTT_PATH = "test_channel"

class Window(QWidget):
    def __init__(self):
        print "In init"
        super(Window, self).__init__()
        self.setWindowTitle("Image")
        self.home()

    def home(self):
        print "home"
        label = QLabel(self)
        client.connect(MQTT_SERVER, 1883)
        client.loop_start()
        print "home: After client"
        self.show()

    def on_connect(self, client, userdata, rc):
        print "on_connect"
        print "Connected with result code: " + str(rc)
        client.subscribe(MQTT_PATH)

    def on_message(self, client, userdata, msg):
        print "on_message"
        #print "Topic: ", msg.topic + '\nMessage: ' + msg.payload
        nparr = np.fromstring(msg.payload.decode('base64'), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

        print 'debug4'
        # Testing to convert opencv image to pixmap
        rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print 'Debug5'
        convertToQtFormat = QImage(rgbImage, rgbImage.shape[1], rgbImage.shape[0], rgbImage.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(convertToQtFormat)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        self.show()
        print "Recieved and Decoded"


if __name__ == "__main__":
    #global client = mqtt.Client()
    global client
    client = mqtt.Client()

    app = QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    #client.loop_start()
    sys.exit(app.exec_())
