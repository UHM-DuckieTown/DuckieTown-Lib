import sys
import numpy as np
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        #self.button()
        self.center()
        self.setWindowTitle('Simple')
        self.show()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class Image(QWidget):
    def __init__(self):
        super(Image, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('convertToQtFormat')
        label = QLabel(self)
        rgbImage = cv2.imread('test.jpg')
        print rgbImage
        #pixmap = QPixmap('test.jpg')
        #rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(rgbImage, rgbImage.shape[1], rgbImage.shape[0], rgbImage.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(convertToQtFormat)
        #pixmap = pixmap.scaled(640,400, Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Image()
    sys.exit(app.exec_())
