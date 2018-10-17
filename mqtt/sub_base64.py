import paho.mqtt.client as mqtt
import numpy as np
import cv2
import base64
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


MQTT_SERVER = "2607:f278:410e:5:8f:b33:3bf:ffa0"
MQTT_PATH = "test_channel"

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def run(self):
        client = mqtt.Client()
        print "In thread run"
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        print "After connect and messages"
        client.loop_start()
        client.connect(MQTT_SERVER, 1883, 60)


    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print "In on_connect"
        print "Connected with result code "+str(rc)

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_PATH)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        #print msg.topic+" sent "+str(msg.payload)
        print "In on_message"
        nparr = np.fromstring(msg.payload.decode('base64'), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

        print 'debug4'
    # Testing to convert opencv image to pixmap
        rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print 'Debug5'
        convertToQtFormat = QImage(rgbImage, rgbImage.shape[1], rgbImage.shape[0], rgbImage.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()

        print 'Debug6'
        self.changePixmap.emit(convertToQtFormat)
        print convertToQtFormat
        print 'Debug7'

        # height, width, channel = img.shape
        # bytesPerLine= 3 * width
        # qImg = QImage(img.data,width,height,bytesPerLine, QImage.Format_RGB888)
        # print 'height: ' + str(height)
        # print 'Width: ' + str(width)
        # print 'Channel: ' + str(channel)

        #pixmap = QPixmap(convertToQtFormat.scaled(640,480))
        print "Recieved and Decoded"
        #cv2.imshow('From Source', img)

        cv2.waitKey(1)

class App(QWidget):
    def __init__(self):
        super(App,self).__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)
        # create a label
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = Thread.on_connect
    client.on_message = Thread.on_message
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    client.loop_start()
    sys.exit(app.exec_())



# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
