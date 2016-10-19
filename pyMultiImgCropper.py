# -*- coding: utf-8 -*-

"""
pyMultiImgCropper.py
version: 0.01
@author: mhr380

"""

import sys
import os
import datetime

from PIL import Image
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
        self.image = QtGui.QImage("./initialImg.png")

        self.pixlabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.pixlabel.resize(self.image.size())

        self.hbox1.addWidget(self.pixlabel)

        self.img_num = 1
        self.num = 0
        self.path_list = []

        self.initial_pt = [0, 0]
        self.end_pt     = [0, 0]

        self.flg_square = False
        self.flg_allowCrop = False

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_B:
            self.num -= 1
            if self.num < 0:
                self.num = self.img_num - 1
            self.showImg(self.img_list, self.num)
        
        if event.key() == QtCore.Qt.Key_N:
            self.num += 1
            if self.num >= self.img_num:
                self.num = 0 
            self.showImg(self.img_list, self.num)

        if event.key() == QtCore.Qt.Key_Escape:
            self.showImg(self.img_list)
            
        if event.key() == QtCore.Qt.Key_Q:
            self.close()
        
        if event.key() == QtCore.Qt.Key_Shift:
            self.flg_square = True
           
        if event.key() == QtCore.Qt.Key_S:
            self.saveCroppedImage()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        self.flg_allowCrop = True
        self.urls = event.mimeData().urls()
        self.file_num = len(self.urls)

        self.path_list = [str(url.path()[1:]) for url in self.urls]
        self.img_num = len(self.path_list)
        
        for num in range(self.img_num):
            pilimg = Image.open(self.path_list[num])
            pilimg = pilimg.convert("RGB")
            npimg = np.array(pilimg)
            self.img_list.append(npimg)
       
        self.showImg(self.img_list)

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
        self.cropImage()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter()

        painter.begin(self)

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

    def showImg(self, img_list, num=0):

        img = img_list[num]
        h, w, ch = img.shape
        self.h, self.w = h, w
        self.resize(w, h)
        bytesPerLine = 3 * w
            
        self.image = QtGui.QImage(img.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)

        self.pixlabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.pixlabel.resize(self.image.size())
    
    def cropImage(self):
        
        mask = np.zeros((self.h, self.w))

        ipx = self.initial_pt[0]
        ipy = self.initial_pt[1]
        epx = self.end_pt[0]
        epy = self.end_pt[1] 
        
        self.ipx, self.ipy = ipx, ipy
        self.epx, self.epy = epx, epy
        
        mask[ipy: epy, ipx: epx] = 1

        cropped_img_list = []
        if self.flg_allowCrop:
            for n, img in enumerate(self.img_list):
                cropped_img = img.copy()
                cropped_img[mask == 0] = 0 
                cropped_img_list.append(cropped_img)
                
        self.showImg(cropped_img_list)

    def saveCroppedImage(self):
        
        ipx = self.ipx
        ipy = self.ipy
        epx = self.epx
        epy = self.epy

        today = datetime.date.today()

        srcpath = self.path_list[0] 

        srcdir = os.path.dirname(srcpath) + "/"
        outdir = srcdir + str(today) + "_"
        
        suffix = 0
        print outdir + str("{0:03d}".format(suffix))
        while os.path.exists(outdir + str("{0:03d}".format(suffix))):
            suffix = suffix + 1
        
        outdir = outdir + str("{0:03d}".format(suffix))
        os.mkdir(outdir)

        if self.flg_allowCrop:
            for n, img in enumerate(self.img_list):
                pilimg = Image.fromarray(img[ ipy: epy, ipx: epx, :])

                filename = os.path.basename(self.path_list[n])
                pilimg.save(os.path.join(outdir, filename))
    
if __name__ == "__main__":
        
    app = QtGui.QApplication(sys.argv)

    w = MainWidget()
    w.show()
    exit(app.exec_())
