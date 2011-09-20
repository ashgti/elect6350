#!/usr/bin/env python

import numpy as np
from matplotlib import use
use('AGG')
from matplotlib.transforms import Bbox
from matplotlib.path import Path
from matplotlib.patches import Rectangle
from matplotlib.pylab import *

from PySide import QtCore, QtGui

class PlotWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        
        closeButton = QtGui.QPushButton("&Close")
        closeButton.clicked.connect(self.close)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.imageLabel)
        layout.addWidget(closeButton)
        self.setLayout(layout)
        
        self.setWindowTitle("Plots")
        
        self.first_time = True
    
    def plot(self, *args):
        """Pasthrough"""
        x, y = args
        plot(x, y)
        self.update()
    
    def plotHeading(self, headings, time):
        """Plots heading"""
        if self.first_time:
            self.first_time = False
        else:
            return
        print(headings, time)
        plot(heading, time)
        self.update()
    
    def paintEvent(self, event):
        gcf().canvas.draw()
        
        stringBuffer = gcf().canvas.buffer_rgba(0,0)
        l, b, w, h = gcf().bbox.bounds
        qImage = QtGui.QImage(stringBuffer,
                              w,
                              h, 
                              QtGui.QImage.Format_ARGB32)
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))
    

if __name__ == '__main__':
    import sys
    
    app = QtGui.QApplication(sys.argv)
    plot_window = PlotWindow()
    plot_window.plot([1,2,3,4],[1,4,9,16])
    plot_window.show()
    sys.exit(app.exec_())
