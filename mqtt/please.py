import paho.mqtt.client as mqtt
import numpy as np
import cv2
import base64
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


MQTT_SERVER = "192.168.0.106"
MQTT_PATH = "test_channel"


class App(QWidget):
    client_message = pyqtSignal(QImage)

    def __init__(self,mqtt_client):
        super(App,self).__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 240
        self._client = mqtt_client
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        #self._client.on_message = lambda c, d, msg: self.client_message.emit(msg)
        #self.client_message.connect(self.on_message)

        self.client_message.connect(self.setImage)
        self.resize(1800,1200)
        # create a label
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)

    def on_message(self, client, userdata, msg):
        #print msg.topic+" sent "+str(msg.payload)
        #print "In on_message"
        nparr = np.fromstring(msg.payload.decode('base64'), np.uint8)
        rgbImage = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

        #print 'debug4'
    # Testing to convert opencv image to pixmap
        #rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #print 'Debug5'
        convertToQtFormat = QImage(rgbImage, rgbImage.shape[1], rgbImage.shape[0], rgbImage.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()

        #print 'Debug6'
        self.client_message.emit(convertToQtFormat)
        #print convertToQtFormat
        #print 'Debug7'

    def on_connect(self, client, userdata, flags, rc):
        print "In on_connect"
        print "Connected with result code "+str(rc)

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_PATH)

if __name__ == '__main__':
    client = mqtt.Client()

    app = QApplication(sys.argv)
    ex = App(client)
    ex.show()

    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_start()
    try:
        sys.exit(app.exec_())
    finally:
        client.loop_stop()



# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
