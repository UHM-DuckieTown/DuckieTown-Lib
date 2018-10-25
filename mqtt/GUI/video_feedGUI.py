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

MQTT_SERVER = "168.105.254.101"
MQTT_PATH1 = "video_channel1"
MQTT_PATH2 = "video_channel2"
MQTT_PATH3 = "text_channel1"
MQTT_PATH4 = "text_channel2"

class MyApp(QMainWindow):
    client_message = pyqtSignal(QImage)

    def __init__(self, mqtt_client):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._client = mqtt_client
        self.initUI()
        self.ui.pushButton.clicked.connect(self.SendMessage)

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.ui.label_3.setPixmap(QPixmap.fromImage(image))
        self.ui.label_4.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message

        self.client_message.connect(self.setImage)

        self.ui.label_3 = QLabel(self)
        self.ui.label_3.resize(520, 461)

        self.ui.label_4= QLabel(self)
        self.ui.label_4.resize(520, 461)

    def on_message(self, client, userdata, msg):
        if msg.topic == MQTT_PATH1:
            nparr = np.fromstring(msg.payload.decode('base64'), np.uint8)
            rgbImage = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
            convertToQtFormat = QImage(rgbImage, rgbImage.shape[1], rgbImage.shape[0], rgbImage.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
            self.client_message.emit(convertToQtFormat)
        elif msg.topic == MQTT_PATH2:
            nparr = np.fromstring(msg.payload.decode('base64'), np.uint8)
            rgbImage = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
            convertToQtFormat = QImage(rgbImage, rgbImage.shape[1], rgbImage.shape[0], rgbImage.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
            self.client_message.emit(convertToQtFormat)

    def on_connect(self, client, userdata, flags, rc):
        print "Connected with result code "+str(rc)
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
