import sys
import numpy as np
import cv2
import base64
import PyQt5
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#Import Ui_MainWindow class from DuckieTown_GUI.py
from DuckieTown_GUI import Ui_MainWindow

#Set the IP of the Broker
MQTT_SERVER = "localhost"

#Subrcibed-Topics
#Main feeds to show Line Tracker Images are sent along thesse topics
#Recieved as a text string
DUCK1_FEED = "duckiefeed/duck1/feed1"
DUCK2_FEED = "duckiefeed/duck2/feed1"

#Secondary feeds to show Raw, Edges, Line Tracker Images, White, and Yellow Mask are sent along these topics
#Recieved as a text string
DUCK1_FEED2 = "duckiefeed/duck1/feed2"
DUCK2_FEED2 = "duckiefeed/duck2/feed2"

#Published-Topics
#Slider Values and Commands are sent along these topics
DUCK1_TEXT = "duckietext/duck1/text"
DUCK2_TEXT = "duckietext/duck2/text"

#Create a class for the Qt Main Window
class MyApp(QMainWindow):

    #Create PyQt Signals for when the QImage is updated.
    #A PyQt Signal emmits a signal to connected PyQt Slots, which are callable functions
    #The QImage class provides an image representation with the ability to directly access the pixel data.

    client_message = pyqtSignal(QImage)

    #Create the method to initialize the Main Window
    def __init__(self, mqtt_client):
        super(MyApp, self).__init__()
        #Make the UI the Class Created from QT Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Create a client instance
        self._client = mqtt_client
        self.initUI()
        #Bind the SendMessage function to the enter key
        self.ui.CommandBox.returnPressed.connect(self.SendMessage)
        #Bind the SendMessage function to the Send button by the Command Box
        self.ui.Send_Button.clicked.connect(self.SendMessage)
        #Bind the SetIP function to the enter key
        self.ui.IPBox.returnPressed.connect(self.SetIP)
        #Bind the SetIP function to the Set IP button by the IP Box
        self.ui.SetIP_Button.clicked.connect(self.SetIP)
        #Bind the Slider function to when the value of the Slider of Duck 1 is changed
        self.ui.Duck1_Slider.valueChanged.connect(self.Slider)
        #Bind the Slider function to when the value of the Slider of Duck 2 is changed
        self.ui.Duck2_Slider.valueChanged.connect(self.Slider2)

    #Python decorator to explicitly mark a Python method as being a Qt slot.
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.ui.Duck1_Feed.setPixmap(QPixmap.fromImage(image).scaled(447,309))

    def initUI(self):
        #Bind on_connect callback to client
        self._client.on_connect = self.on_connect

        self._client.on_message_duck = self.on_message_duck
        #Connecting signals to slots
        self.client_message.connect(self.setImage)

        self._client.message_callback_add("duckiefeed/#", self.on_message_duck)

        #Adjust the feed position to be at the top left
        self.ui.Duck1_Feed = QLabel(self)
        self.ui.Duck1_Feed.resize(447, 309)
        self.ui.Duck1_Feed.move(30, 50)

        #Adjust the feed position to be at the top right
        self.ui.Duck1_Feed2 = QLabel(self)
        self.ui.Duck1_Feed2.resize(447, 309)
        self.ui.Duck1_Feed2.move(482, 0)
        self.ui.Duck1_Feed2.move(482, 50)

        #Adjust the feed position to be at the bottom left
        self.ui.Duck2_Feed = QLabel(self)
        self.ui.Duck2_Feed.resize(447, 309)
        self.ui.Duck2_Feed.move(30, 417)

        #Adjust the feed position to be at the bottom right
        self.ui.Duck2_Feed2 = QLabel(self)
        self.ui.Duck2_Feed2.resize(447, 309)
        self.ui.Duck2_Feed2.move(482, 417)

    #Function for when the encoded string is received from DUCK1_FEED
    def on_message_duck(self, client, userdata, msg):
        #Decode the encoded string from a ascii-value string to an nparray in memory buffer using base64 decode
        nparr = np.fromstring(msg.payload.decode('base64'), np.uint8)
        #Decode the nparray from the memory buffer to an image using imdecode
        image = cv2.imdecode(nparr, 1)
        #Convert the image to be compatible with PqQt
        convertToQtFormat = QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        #Emit a signal for the Slot
        self.client_message.emit(convertToQtFormat)

    #Function for when the broker responds to our connection request
    def on_connect(self, client, userdata, flags, rc):
        print "Connected with result code "+str(rc)
        # Defines Callbacks that handle incoming messages for specific topics
        # on_message_duck1 will be called when an message from DUCK1_FEED arrives
        client.message_callback_add(DUCK1_FEED, self.on_message_duck)
        #Subscribes the client to Video Feeds
        client.subscribe("duckiefeed/#", 0)

    #Function to send a message to the ducks,
    def SendMessage(self):
        #Bind the message variable to what is typed in the command box
        message = self.ui.CommandBox.text()
        #If you want to send a message to Duck 1 only
        if self.ui.Duck1_Check.isChecked() and not self.ui.Duck2_Check.isChecked():
            #Publish onto Duck 1 Text Topic
            self._client.publish(DUCK1_TEXT, message)
        #If you want to send a message to Duck 2 only
        elif self.ui.Duck2_Check.isChecked() and not self.ui.Duck1_Check.isChecked():
            #Publish onto Duck 2 Text Topic
            self._client.publish(DUCK2_TEXT, message)
        #If you want to send a message to Duck 1 and Duck 2
        elif self.ui.Duck1_Check.isChecked() and self.ui.Duck2_Check.isChecked():
            #Publish onto Duck 1 Text Topic
            self._client.publish(DUCK1_TEXT, message)
            #Publish onto Duck 2 Text Topic
            self._client.publish(DUCK2_TEXT, message)
        #Clear the command box
        self.ui.CommandBox.clear()

    #Function to set the IP to desired IP
    def SetIP(self):
        #Bind the MQTT_SERVER variable to what is typed in the IP box
        MQTT_SERVER = self.ui.IPBox.text()
        #Clear the IP box
        self.ui.IPBox.clear()
        #print "IP set to " + MQTT_SERVER

    #Function to send the desired value of slider to Duck 1
    def Slider(self):
        #Bind the value variable to the value of the slider
        value = str(self.ui.Duck1_Slider.value())
        #Publish onto the Duck 1 Text Feed
        self._client.publish(DUCK1_TEXT, value)
        #print "slider 1:" + str(self.ui.Duck1_Slider.value())

    #Function to send the desired value of slider to Duck 2
    def Slider2(self):
        #Bind the value variable to the value of the slider
        value = str(self.ui.Duck2_Slider.value())
        #Publish onto the Duck 1 Text Feed
        self._client.publish(DUCK2_TEXT, value)
        #print "slider 2:" + str(self.ui.Duck2_Slider.value())


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
