import sys
import numpy as np
import cv2
import base64
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import paho.mqtt.client as mqtt
from videofeed import Ui_MainWindow

MQTT_SERVER = "168.105.252.131"
MQTT_PATH1 = "video_channel1"
MQTT_PATH2 = "video_channel2"
MQTT_PATH3 = "text_channel1"
MQTT_PATH4 = "text_channel2"

class MyApp(QMainWindow):
    client_message1 = pyqtSignal(QImage)
    client_message2 = pyqtSignal(QImage)

    def __init__(self, mqtt_client):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._client = mqtt_client
        self.initUI()
        self.ui.pushButton.clicked.connect(self.SendMessage)

    @pyqtSlot(QImage)
    def setImage1(self, image1):
        self.ui.label_3.setPixmap(QPixmap.fromImage(image1).scaled(480,369))
    @pyqtSlot(QImage)
    def setImage2(self, image2):
        self.ui.label_4.setPixmap(QPixmap.fromImage(image2))

    def initUI(self):

        self._client.on_connect = self.on_connect
        self._client.on_message_duck1 = self.on_message_duck1
        self._client.on_message_duck2 = self.on_message_duck2

        self.client_message1.connect(self.setImage1)
        self.client_message2.connect(self.setImage2)

        self._client.message_callback_add(MQTT_PATH1, self.on_message_duck1)
        self._client.message_callback_add(MQTT_PATH2, self.on_message_duck2)

        self.ui.label_3 = QLabel(self)
        self.ui.label_3.resize(488, 520)

        self.ui.label_4 = QLabel(self)
        self.ui.label_4.resize(487, 520)
        self.ui.label_4.move(510, 0)

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

    def on_connect(self, client, userdata, flags, rc):
        print "Connected with result code "+str(rc)
        client.message_callback_add(MQTT_PATH1, self.on_message_duck1)
        client.message_callback_add(MQTT_PATH2, self.on_message_duck2)
        client.subscribe([(MQTT_PATH1,1),(MQTT_PATH2,2)])

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
