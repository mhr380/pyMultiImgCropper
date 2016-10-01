# -*- coding: utf-8 -*-

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
        self.setWindowTitle(u"D&D")
        self.resize(320, 240)

        self.vbox = QtGui.QVBoxLayout()
        self.hbox1 = QtGui.QHBoxLayout()

        self.setAcceptDrops(True)

        self.img_list = []

        self.hbox1 = QtGui.QHBoxLayout()

        self.pixlabel = QtGui.QLabel(self)
        self.pixmap = QtGui.QPixmap("./initialImg.png")
        self.pixlabel.setPixmap(self.pixmap)
        self.pixlabel.resize(self.pixmap.size())

        self.hbox1.addWidget(self.pixlabel)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.urls = event.mimeData().urls()
        self.file_num = len(self.urls)

        self.path_list = [str(url.path()[1:]) for url in self.urls]

        for path in self.path_list:
            if os.path.exists(path):
                img = cv2.imread(path, 1) 
                self.img_list.append(img)
                
            height, width, ch = self.img_list[0].shape
            self.resize(width + 10, height + 30)
        
        self.showImg()
    
    def showImg(self):
        self.pixmap = QtGui.QPixmap(self.path_list[0])
        self.pixlabel.setPixmap(self.pixmap)
        self.pixlabel.resize(self.pixmap.size())


if __name__ == "__main__":
        
    app = QtGui.QApplication(sys.argv)

    w = MainWidget()
    w.show()
    exit(app.exec_())
