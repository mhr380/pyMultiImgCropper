# -*- coding: utf-8 -*-

"""
pyMultiImgCropper.py
version: 1.0
@author: mhr380

"""

import sys
import os

import cv2
import numpy as np

from PyQt4 import QtCore
from PyQt4 import QtGui

class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(u"MultiImageCropper")

        self.scene = QtGui.QGraphicsScene()

        self.vbox = QtGui.QVBoxLayout()
        self.hbox1 = QtGui.QHBoxLayout()

        self.setAcceptDrops(True)

        self.img_list = []

        self.hbox1 = QtGui.QHBoxLayout()

        self.pixlabel = QtGui.QLabel(self)
        #self.pixmap = QtGui.QPixmap("./initialImg.png")
        self.image = QtGui.QImage("./initialImg.png")
        #self.pixlabel.resize(self.pixmap.size())

        #self.pixlabel.setPixmap(self.pixmap)
        self.pixlabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.pixlabel.resize(self.image.size())

        self.hbox1.addWidget(self.pixlabel)

        self.img_num = 1
        self.num = 0
        self.path_list = []

        self.initial_pt = [0, 0]
        self.end_pt     = [0, 0]

        self.flg_square = False

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_B:
            self.num -= 1
            if self.num < 0:
                self.num = self.img_num - 1
            self.showImg(self.num)
        
        if event.key() == QtCore.Qt.Key_N:
            self.num += 1
            if self.num >= self.img_num:
                self.num = 0 
            self.showImg(self.num)

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        
        if event.key() == QtCore.Qt.Key_Shift:
            self.flg_square = True

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.urls = event.mimeData().urls()
        self.file_num = len(self.urls)

        self.path_list = [str(url.path()[1:]) for url in self.urls]
        self.img_num = len(self.path_list)

        for path in self.path_list:
            if os.path.exists(path):
                img = cv2.imread(path, 1) 
                self.img_list.append(img)
            height, width, ch = self.img_list[0].shape
            self.resize(width, height)
        
        self.showImg()

    def mousePressEvent(self, event):
        self.initial_pt = event.pos().x(), event.pos().y()
        self.update() 
    
    def mouseMoveEvent(self, event):
        self.end_pt = event.pos().x(), event.pos().y()
        self.update()

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.end_pt = event.pos().x(), event.pos().y()
        self.update()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter()

        painter.begin(self.image)

        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.NoBrush)

        ipx = self.initial_pt[0]
        ipy = self.initial_pt[1]
        epx = self.end_pt[0]
        epy = self.end_pt[1] 

        if self.flg_square == True:
            if epx - ipx < epy - ipy:
                size = epx - ipx
            else:
                size = epy - ipy

            painter.drawRect(ipx, ipy, size, size)
        else:
            painter.drawRect(ipx, ipy, epx - ipx, epy - ipy)
        
        self.update()
        painter.end()

    def showImg(self, num=0):
        #self.pixmap = QtGui.QPixmap(self.path_list[num])
        if self.img_num > 1:
            cvimg = cv2.imread(self.path_list[num], 1)
            h, w, ch = cvimg.shape
            bytesPerLine = 3 * w
            #img = self.rgb2bgr(cvimg)

            self.image = QtGui.QImage(cvimg.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)

        #self.pixlabel.setPixmap(self.pixmap)
        self.pixlabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.pixlabel.resize(self.image.size())
    
    def rgb2bgr(self, img):
        h, w, ch = img.shape
        swappedimg = np.zeros((h, w, ch))

        swappedimg[:, :, 0] = img[:, :, 2]
        swappedimg[:, :, 1] = img[:, :, 1]
        swappedimg[:, :, 2] = img[:, :, 0]

        return swappedimg

if __name__ == "__main__":
        
    app = QtGui.QApplication(sys.argv)

    w = MainWidget()
    w.show()
    exit(app.exec_())