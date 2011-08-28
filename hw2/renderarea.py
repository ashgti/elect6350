import sys
from PySide import QtCore, QtGui

class RenderArea(QtGui.QWidget):
    """Render area for rendering the robot"""
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        newFont = self.font()
        newFont.setPixelSize(12)
        self.setFont(newFont)
        
        fontMetrics = QtGui.QFontMetrics(newFont)
        self.xBoundingRect = fontMetrics.boundingRect(self.tr("x"))
        self.yBoundingRect = fontMetrics.boundingRect(self.tr("y"))
    
    def paintEvent(self, event):
        """Handles painting the render area"""
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(event.rect(), QtGui.QBrush(QtCore.Qt.black))
        
        painter.save()
        # self.drawCoordinates(painter)
        self.drawGlobalCoordinates(painter)
        painter.restore()
        
        painter.translate(self.size().width()/2, self.size().height()/2)
        
        painter.setPen(QtCore.Qt.yellow)
        painter.drawRect(-50, -50, 100, 100)
        
        painter.end()
    
    def drawCoordinates(self, painter):
        painter.setPen(QtCore.Qt.red)
        
        painter.drawLine(0, 0, 50, 0)
        painter.drawLine(48, -2, 50, 0)
        painter.drawLine(48, 2, 50, 0)
        painter.drawText(60 - self.xBoundingRect.width() / 2,
                         -2 + self.xBoundingRect.height() / 2, self.tr("Y"))
        
        painter.drawLine(0, 0, 0, -50)
        painter.drawLine(-2, -48, 0, -50)
        painter.drawLine(2, -48, 0, -50)
        painter.drawText(0 - self.yBoundingRect.width() / 2,
                         -60 + self.yBoundingRect.height() / 2, self.tr("X"))
    
    def drawGlobalCoordinates(self, painter):
        offset_x = 10
        offset_y = self.size().height() - 10
        painter.translate(offset_x, offset_y)
        
        painter.setPen(QtCore.Qt.red)
        
        painter.drawLine(0, 0, 50, 0)
        painter.drawLine(48, -2, 50, 0)
        painter.drawLine(48, 2, 50, 0)
        painter.drawText(60 - self.xBoundingRect.width() / 2,
                         -2 + self.xBoundingRect.height() / 2, self.tr("X"))
        
        painter.setPen(QtCore.Qt.green)
        
        painter.drawLine(0, 0, 0, -50)
        painter.drawLine(-2, -48, 0, -50)
        painter.drawLine(2, -48, 0, -50)
        painter.drawText(0 - self.yBoundingRect.width() / 2,
                         -60 + self.yBoundingRect.height() / 2, self.tr("Y"))
    
