import sys
import numpy as np
import cv2
import base64
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import paho.mqtt.client as mqtt
from feed import Ui_MainWindow

MQTT_SERVER = "192.168.0.100"
MQTT_PATH1 = "video_channel1"
MQTT_PATH2 = "video_channel2"
MQTT_PATH3 = "text_channel1"
MQTT_PATH4 = "text_channel2"
MQTT_PATH5 = "video_channel3"
MQTT_PATH6 = "video_channel4"

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
        self.ui.pushButton.clicked.connect(self.SendMessage)

    @pyqtSlot(QImage)
    def setImage1(self, image1):
        self.ui.label_3.setPixmap(QPixmap.fromImage(image1).scaled(472,309))
    @pyqtSlot(QImage)
    def setImage2(self, image2):
        self.ui.label_4.setPixmap(QPixmap.fromImage(image2).scaled(472,309))
    @pyqtSlot(QImage)
    def setImage3(self, image3):
        self.ui.label_7.setPixmap(QPixmap.fromImage(image3).scaled(472,309))
    @pyqtSlot(QImage)
    def setImage4(self, image4):
        self.ui.label_8.setPixmap(QPixmap.fromImage(image4).scaled(472,309))

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

        self._client.message_callback_add(MQTT_PATH1, self.on_message_duck1)
        self._client.message_callback_add(MQTT_PATH2, self.on_message_duck2)
        self._client.message_callback_add(MQTT_PATH1, self.on_message_duck3)
        self._client.message_callback_add(MQTT_PATH2, self.on_message_duck4)

        self.ui.label_3 = QLabel(self)
        self.ui.label_3.resize(472, 309)

        self.ui.label_4 = QLabel(self)
        self.ui.label_4.resize(472, 309)
        self.ui.label_4.move(510, 0)

        self.ui.label_7 = QLabel(self)
        #self.ui.label_7.resize(472, 309)
        self.ui.label_7.resize(472, 309)
        self.ui.label_7.move(0, 309)

        self.ui.label_8 = QLabel(self)
        self.ui.label_8.resize(472, 309)
        self.ui.label_8.move(510, 309)


    def on_message_duck1(self, client, userdata, msg):
        nparr1 = np.fromstring(msg.payload.decode('base64'), np.uint8)
        rgbImage1 = cv2.imdecode(nparr1, cv2.IMREAD_ANYCOLOR)
        convertToQtFormat1 = QImage(rgbImage1, rgbImage1.shape[1], rgbImage1.shape[0], rgbImage1.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        self.client_message1.emit(convertToQtFormat1)

    def on_message_duck2(self, client, userdata, msg):
        nparr2 = np.fromstring(msg.payload.decode('base64'), np.uint8)
        rgbImage2 = cv2.imdecode(nparr2, cv2.IMREAD_ANYCOLOR)
        convertToQtFormat2 = QImage(rgbImage2, rgbImage2.shape[1], rgbImage2.shape[0], rgbImage2.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        self.client_message2.emit(convertToQtFormat2)

    def on_message_duck3(self, client, userdata, msg):
        nparr3 = np.fromstring(msg.payload.decode('base64'), np.uint8)
        rgbImage3 = cv2.imdecode(nparr3, cv2.IMREAD_ANYCOLOR)
        convertToQtFormat3 = QImage(rgbImage3, rgbImage3.shape[1], rgbImage3.shape[0], rgbImage3.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        self.client_message3.emit(convertToQtFormat3)

    def on_message_duck4(self, client, userdata, msg):
        nparr4 = np.fromstring(msg.payload.decode('base64'), np.uint8)
        rgbImage4 = cv2.imdecode(nparr4, cv2.IMREAD_ANYCOLOR)
        convertToQtFormat4 = QImage(rgbImage4, rgbImage4.shape[1], rgbImage4.shape[0], rgbImage4.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        self.client_message4.emit(convertToQtFormat4)

    def on_connect(self, client, userdata, flags, rc):
        print "Connected with result code "+str(rc)
        client.message_callback_add(MQTT_PATH1, self.on_message_duck1)
        client.message_callback_add(MQTT_PATH2, self.on_message_duck2)
        client.message_callback_add(MQTT_PATH5, self.on_message_duck3)
        client.message_callback_add(MQTT_PATH6, self.on_message_duck4)
        client.subscribe([(MQTT_PATH1,0),(MQTT_PATH2,0),(MQTT_PATH5,0),(MQTT_PATH6,0)])

    def SendMessage(self):
        message = self.ui.plainTextEdit.toPlainText()
        if self.ui.checkBox.isChecked() and not self.ui.checkBox_2.isChecked():
            self._client.publish(MQTT_PATH3, message)
        elif self.ui.checkBox_2.isChecked() and not self.ui.checkBox.isChecked():
            self._client.publish(MQTT_PATH4, message)
        elif self.ui.checkBox.isChecked() and self.ui.checkBox_2.isChecked():
            self._client.publish(MQTT_PATH3, message)
            self._client.publish(MQTT_PATH4, message)

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
