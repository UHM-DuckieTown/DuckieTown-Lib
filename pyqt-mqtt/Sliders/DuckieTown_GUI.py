# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1047, 894)
        MainWindow.setBaseSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Send_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Send_Button.setGeometry(QtCore.QRect(830, 800, 71, 41))
        self.Send_Button.setObjectName("Send_Button")
        self.Duck1_Check = QtWidgets.QCheckBox(self.centralwidget)
        self.Duck1_Check.setGeometry(QtCore.QRect(910, 800, 70, 17))
        self.Duck1_Check.setObjectName("Duck1_Check")
        self.Duck2_Check = QtWidgets.QCheckBox(self.centralwidget)
        self.Duck2_Check.setGeometry(QtCore.QRect(910, 820, 70, 17))
        self.Duck2_Check.setObjectName("Duck2_Check")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 50, 901, 311))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Duck1_Feed = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.Duck1_Feed.setBaseSize(QtCore.QSize(400, 400))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Duck1_Feed.setFont(font)
        self.Duck1_Feed.setText("")
        self.Duck1_Feed.setObjectName("Duck1_Feed")
        self.horizontalLayout.addWidget(self.Duck1_Feed)
        self.Duck1_Feed2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.Duck1_Feed2.setText("")
        self.Duck1_Feed2.setObjectName("Duck1_Feed2")
        self.horizontalLayout.addWidget(self.Duck1_Feed2)
        self.Duck1_Label = QtWidgets.QLabel(self.centralwidget)
        self.Duck1_Label.setGeometry(QtCore.QRect(26, 360, 461, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Duck1_Label.setFont(font)
        self.Duck1_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Duck1_Label.setObjectName("Duck1_Label")
        self.Duck1_Label2 = QtWidgets.QLabel(self.centralwidget)
        self.Duck1_Label2.setGeometry(QtCore.QRect(500, 360, 461, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Duck1_Label2.setFont(font)
        self.Duck1_Label2.setAlignment(QtCore.Qt.AlignCenter)
        self.Duck1_Label2.setObjectName("Duck1_Label2")
        self.SetIP_Button = QtWidgets.QPushButton(self.centralwidget)
        self.SetIP_Button.setGeometry(QtCore.QRect(890, 10, 75, 23))
        self.SetIP_Button.setObjectName("SetIP_Button")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(24, 410, 901, 311))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Duck2_Feed = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.Duck2_Feed.setBaseSize(QtCore.QSize(400, 400))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Duck2_Feed.setFont(font)
        self.Duck2_Feed.setText("")
        self.Duck2_Feed.setObjectName("Duck2_Feed")
        self.horizontalLayout_3.addWidget(self.Duck2_Feed)
        self.Duck2_Feed2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.Duck2_Feed2.setText("")
        self.Duck2_Feed2.setObjectName("Duck2_Feed2")
        self.horizontalLayout_3.addWidget(self.Duck2_Feed2)
        self.Duck2_Label2 = QtWidgets.QLabel(self.centralwidget)
        self.Duck2_Label2.setGeometry(QtCore.QRect(504, 730, 461, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Duck2_Label2.setFont(font)
        self.Duck2_Label2.setAlignment(QtCore.Qt.AlignCenter)
        self.Duck2_Label2.setObjectName("Duck2_Label2")
        self.Duck2_Label = QtWidgets.QLabel(self.centralwidget)
        self.Duck2_Label.setGeometry(QtCore.QRect(30, 730, 461, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Duck2_Label.setFont(font)
        self.Duck2_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Duck2_Label.setObjectName("Duck2_Label")
        self.Duck1_MaskW_Label = QtWidgets.QLabel(self.centralwidget)
        self.Duck1_MaskW_Label.setGeometry(QtCore.QRect(970, 120, 61, 16))
        self.Duck1_MaskW_Label.setObjectName("Duck1_MaskW_Label")
        self.Duck1_Edges_Label = QtWidgets.QLabel(self.centralwidget)
        self.Duck1_Edges_Label.setGeometry(QtCore.QRect(970, 270, 47, 13))
        self.Duck1_Edges_Label.setObjectName("Duck1_Edges_Label")
        self.Duck1_MaskY_Label = QtWidgets.QLabel(self.centralwidget)
        self.Duck1_MaskY_Label.setGeometry(QtCore.QRect(970, 50, 61, 16))
        self.Duck1_MaskY_Label.setObjectName("Duck1_MaskY_Label")
        self.Duck1_Raw_Label = QtWidgets.QLabel(self.centralwidget)
        self.Duck1_Raw_Label.setGeometry(QtCore.QRect(970, 350, 47, 13))
        self.Duck1_Raw_Label.setObjectName("Duck1_Raw_Label")
        self.Duck2_Edges_Label = QtWidgets.QLabel(self.centralwidget)
        self.Duck2_Edges_Label.setGeometry(QtCore.QRect(970, 630, 47, 13))
        self.Duck2_Edges_Label.setObjectName("Duck2_Edges_Label")
        self.Duck2_MaskY_Label = QtWidgets.QLabel(self.centralwidget)
        self.Duck2_MaskY_Label.setGeometry(QtCore.QRect(970, 410, 61, 16))
        self.Duck2_MaskY_Label.setObjectName("Duck2_MaskY_Label")
        self.Duck2_Raw_Label = QtWidgets.QLabel(self.centralwidget)
        self.Duck2_Raw_Label.setGeometry(QtCore.QRect(970, 710, 47, 13))
        self.Duck2_Raw_Label.setObjectName("Duck2_Raw_Label")
        self.Duck2_MaskW_Label = QtWidgets.QLabel(self.centralwidget)
        self.Duck2_MaskW_Label.setGeometry(QtCore.QRect(970, 480, 61, 16))
        self.Duck2_MaskW_Label.setObjectName("Duck2_MaskW_Label")
        self.Duck1_MaskImg_Label = QtWidgets.QLabel(self.centralwidget)
        self.Duck1_MaskImg_Label.setGeometry(QtCore.QRect(970, 200, 61, 16))
        self.Duck1_MaskImg_Label.setObjectName("Duck1_MaskImg_Label")
        self.Duck1_Mask_Label_3 = QtWidgets.QLabel(self.centralwidget)
        self.Duck1_Mask_Label_3.setGeometry(QtCore.QRect(970, 560, 61, 16))
        self.Duck1_Mask_Label_3.setObjectName("Duck1_Mask_Label_3")
        self.Duck1_Slider = QtWidgets.QSlider(self.centralwidget)
        self.Duck1_Slider.setGeometry(QtCore.QRect(940, 50, 22, 311))
        self.Duck1_Slider.setMaximum(4)
        self.Duck1_Slider.setSingleStep(1)
        self.Duck1_Slider.setPageStep(1)
        self.Duck1_Slider.setOrientation(QtCore.Qt.Vertical)
        self.Duck1_Slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.Duck1_Slider.setTickInterval(1)
        self.Duck1_Slider.setObjectName("Duck1_Slider")
        self.Duck2_Slider = QtWidgets.QSlider(self.centralwidget)
        self.Duck2_Slider.setGeometry(QtCore.QRect(940, 410, 22, 311))
        self.Duck2_Slider.setMaximum(4)
        self.Duck2_Slider.setSingleStep(1)
        self.Duck2_Slider.setPageStep(1)
        self.Duck2_Slider.setOrientation(QtCore.Qt.Vertical)
        self.Duck2_Slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.Duck2_Slider.setTickInterval(1)
        self.Duck2_Slider.setObjectName("Duck2_Slider")
        self.CommandBox = QtWidgets.QLineEdit(self.centralwidget)
        self.CommandBox.setGeometry(QtCore.QRect(22, 800, 811, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.CommandBox.setFont(font)
        self.CommandBox.setText("")
        self.CommandBox.setObjectName("CommandBox")
        self.IPBox = QtWidgets.QLineEdit(self.centralwidget)
        self.IPBox.setGeometry(QtCore.QRect(770, 10, 113, 20))
        self.IPBox.setObjectName("IPBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1047, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DuckieTown"))
        self.Send_Button.setText(_translate("MainWindow", "Send"))
        self.Duck1_Check.setText(_translate("MainWindow", "Duck 1"))
        self.Duck2_Check.setText(_translate("MainWindow", "Duck 2"))
        self.Duck1_Label.setText(_translate("MainWindow", "Duck 1"))
        self.Duck1_Label2.setText(_translate("MainWindow", "Duck 1"))
        self.SetIP_Button.setText(_translate("MainWindow", "Set IP"))
        self.Duck2_Label2.setText(_translate("MainWindow", "Duck 2"))
        self.Duck2_Label.setText(_translate("MainWindow", "Duck 2"))
        self.Duck1_MaskW_Label.setText(_translate("MainWindow", "Mask (W)"))
        self.Duck1_Edges_Label.setText(_translate("MainWindow", "Edges"))
        self.Duck1_MaskY_Label.setText(_translate("MainWindow", "Mask (Y)"))
        self.Duck1_Raw_Label.setText(_translate("MainWindow", "Raw"))
        self.Duck2_Edges_Label.setText(_translate("MainWindow", "Edges"))
        self.Duck2_MaskY_Label.setText(_translate("MainWindow", "Mask (Y)"))
        self.Duck2_Raw_Label.setText(_translate("MainWindow", "Raw"))
        self.Duck2_MaskW_Label.setText(_translate("MainWindow", "Mask (W)"))
        self.Duck1_MaskImg_Label.setText(_translate("MainWindow", "Mask Img"))
        self.Duck1_Mask_Label_3.setText(_translate("MainWindow", "Mask Img"))
        self.CommandBox.setPlaceholderText(_translate("MainWindow", "Enter Command..."))
        self.IPBox.setPlaceholderText(_translate("MainWindow", "IP Address"))
