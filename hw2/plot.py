import numpy as np
from matplotlib import use
use('AGG')
from matplotlib.transforms import Bbox
from matplotlib.path import Path
from matplotlib.patches import Rectangle
from matplotlib.pylab import *

from PySide import QtCore, QtGui

class MLPlot(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

    def paintEvent(self, event):
        gcf().canvas.draw()

        stringBuffer = gcf().canvas.buffer_rgba(0,0)
        l, b, w, h = gcf().bbox.bounds
        qImage = QtGui.QImage(stringBuffer,
                              w,
                              h, 
                              QtGui.QImage.Format_ARGB32)


if __name__ == '__main__':
    plot([1,2,3,4],[1,4,9,16])
    app = QtGui.QApplication(sys.argv)
    gcf().canvas.draw()
    
    stringBuffer = gcf().canvas.buffer_rgba(0,0)
    l, b, w, h = gcf().bbox.bounds
    
    qImage = QtGui.QImage(stringBuffer,
                          w,
                          h, 
                          QtGui.QImage.Format_ARGB32)
    scene = QtGui.QGraphicsScene()
    view = QtGui.QGraphicsView(scene)
    pixmap = QtGui.QPixmap.fromImage(qImage)
    pixmapItem = QtGui.QGraphicsPixmapItem(pixmap)
    scene.addItem(pixmapItem)
    view.show()
    
    app.exec_()