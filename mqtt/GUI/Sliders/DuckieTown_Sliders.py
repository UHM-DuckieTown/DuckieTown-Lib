import sys
import numpy as np
import cv2
import base64
import PyQt5
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from DuckieTown_GUI import Ui_MainWindow
import socket

MQTT_SERVER = "localhost"



DUCK1_FEED = "192.168.0.69_feed1"
DUCK1_FEED2 = "192.168.0.69_feed2"
DUCK1_TEXT = "192.168.0.69_text"

DUCK2_FEED = "192.168.0.70_feed1"
DUCK2_FEED2 = "192.168.0.70_feed1"
DUCK2_TEXT = "192.168.0.70_text"

class MyApp(QMainWindow):
    client_message1 = pyqtSignal(QImage)
    client_message2 = pyqtSignal(QImage)
    client_message3 = pyqtSignal(QImage)
    client_message4 = pyqtSignal(QImage)

    def __init__(self, mqtt_client):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._client = mqtt_client
        self.initUI()
        self.ui.CommandBox.returnPressed.connect(self.SendMessage)
        self.ui.Send_Button.clicked.connect(self.SendMessage)
        self.ui.IPBox.returnPressed.connect(self.SetIP)
        self.ui.SetIP_Button.clicked.connect(self.SetIP)
        self.ui.Duck1_Slider.valueChanged.connect(self.Slider)
        self.ui.Duck2_Slider.valueChanged.connect(self.Slider2)

    @pyqtSlot(QImage)
    def setImage1(self, image1):
        self.ui.Duck1_Feed.setPixmap(QPixmap.fromImage(image1).scaled(447,309))
    @pyqtSlot(QImage)
    def setImage2(self, image2):
        self.ui.Duck1_Feed2.setPixmap(QPixmap.fromImage(image2).scaled(447,309))
    @pyqtSlot(QImage)
    def setImage3(self, image3):
        self.ui.Duck2_Feed.setPixmap(QPixmap.fromImage(image3).scaled(447,309))
    @pyqtSlot(QImage)
    def setImage4(self, image4):
        self.ui.Duck2_Feed2.setPixmap(QPixmap.fromImage(image4).scaled(447,309))

    def initUI(self):

        self._client.on_connect = self.on_connect
        self._client.on_message_duck1 = self.on_message_duck1
        self._client.on_message_duck2 = self.on_message_duck2
        self._client.on_message_duck3 = self.on_message_duck3
        self._client.on_message_duck4 = self.on_message_duck4

        self.client_message1.connect(self.setImage1)
        self.client_message2.connect(self.setImage2)
        self.client_message3.connect(self.setImage3)
        self.client_message4.connect(self.setImage4)

        self._client.message_callback_add(DUCK1_FEED, self.on_message_duck1)
        self._client.message_callback_add(DUCK1_FEED2, self.on_message_duck2)
        self._client.message_callback_add(DUCK2_FEED, self.on_message_duck3)
        self._client.message_callback_add(DUCK2_FEED2, self.on_message_duck4)

        self.ui.Duck1_Feed = QLabel(self)
        self.ui.Duck1_Feed.resize(447, 309)
        self.ui.Duck1_Feed.move(30, 50)

        self.ui.Duck1_Feed2 = QLabel(self)
        self.ui.Duck1_Feed2.resize(447, 309)
        self.ui.Duck1_Feed2.move(482, 0)
        self.ui.Duck1_Feed2.move(482, 50)

        self.ui.Duck2_Feed = QLabel(self)
        self.ui.Duck2_Feed.resize(447, 309)
        self.ui.Duck2_Feed.move(30, 417)

        self.ui.Duck2_Feed2 = QLabel(self)
        self.ui.Duck2_Feed2.resize(447, 309)
        self.ui.Duck2_Feed2.move(482, 417)

    def on_message_duck1(self, client, userdata, msg):
        nparr1 = np.fromstring(msg.payload.decode('base64'), np.uint8)
        image1 = cv2.imdecode(nparr1, 1)
        convertToQtFormat1 = QImage(image1, image1.shape[1], image1.shape[0], image1.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        self.client_message1.emit(convertToQtFormat1)
        print "Recieved 1"

    def on_message_duck2(self, client, userdata, msg):
        nparr2 = np.fromstring(msg.payload.decode('base64'), np.uint8)
        image2 = cv2.imdecode(nparr2, 1)
        convertToQtFormat2 = QImage(image2, image2.shape[1], image2.shape[0], image2.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        self.client_message2.emit(convertToQtFormat2)
        print "Recieved 2"

    def on_message_duck3(self, client, userdata, msg):
        nparr3 = np.fromstring(msg.payload.decode('base64'), np.uint8)
        image3 = cv2.imdecode(nparr3, 1)
        convertToQtFormat3 = QImage(image3, image3.shape[1], image3.shape[0], image3.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        self.client_message3.emit(convertToQtFormat3)
        print "Recieved 3"

    def on_message_duck4(self, client, userdata, msg):
        nparr4 = np.fromstring(msg.payload.decode('base64'), np.uint8)
        image4 = cv2.imdecode(nparr4, 1)
        convertToQtFormat4 = QImage(image4, image4.shape[1], image4.shape[0], image4.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        self.client_message4.emit(convertToQtFormat4)
        print "Recieved 4"

    def on_connect(self, client, userdata, flags, rc):
        print "Connected with result code "+str(rc)
        client.message_callback_add(DUCK1_FEED, self.on_message_duck1)
        client.message_callback_add(DUCK1_FEED2, self.on_message_duck2)
        client.message_callback_add(DUCK2_FEED, self.on_message_duck3)
        client.message_callback_add(DUCK2_FEED2, self.on_message_duck4)
        client.subscribe([(DUCK1_FEED,0),(DUCK1_FEED2,0),(DUCK2_FEED,0),(DUCK2_FEED2,0)])

    def SendMessage(self):
        message = self.ui.CommandBox.text()
        if self.ui.Duck1_Check.isChecked() and not self.ui.Duck2_Check.isChecked():
            self._client.publish(DUCK1_TEXT, message)
        elif self.ui.Duck2_Check.isChecked() and not self.ui.Duck1_Check.isChecked():
            self._client.publish(DUCK2_TEXT, message)
        elif self.ui.Duck1_Check.isChecked() and self.ui.Duck2_Check.isChecked():
            self._client.publish(DUCK1_TEXT, message)
            self._client.publish(DUCK2_TEXT, message)
        self.ui.CommandBox.clear()

    def SetIP(self):
        MQTT_SERVER = self.ui.IPBox.text()
        self.ui.IPBox.clear()
        print "IP set to " + MQTT_SERVER

    def Slider(self):
        value = str(self.ui.Duck1_Slider.value())
        self._client.publish(DUCK1_TEXT, value)
        print "slider 1:" + str(self.ui.Duck1_Slider.value())

    def Slider2(self):
        value = str(self.ui.Duck2_Slider.value())
        self._client.publish(DUCK2_TEXT, value)
        print "slider 2:" + str(self.ui.Duck2_Slider.value())


if __name__ == "__main__":
    client = mqtt.Client()
    app = QApplication(sys.argv)
    window = MyApp(client)
    window.show()
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_start()
    try:
        sys.exit(app.exec_())
    finally:
        client.loop_stop()
