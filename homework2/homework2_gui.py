#!/usr/bin/env python

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
    
    def minimumSizeHint(self):
        return QtCore.QSize(600, 600)
    
    def sizeHint(self):
        return QtCore.QSize(600, 600)
    
    def paintEvent(self, event):
        """Handles painting the render area"""
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(event.rect(), QtGui.QBrush(QtCore.Qt.white))
        
        painter.translate(300, 300)
        
        painter.save()
        self.drawCoordinates(painter)
        painter.restore()
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
    

class Window(QtGui.QWidget):
    """Main window"""
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.render_area = RenderArea()
        
        self.render_group = QtGui.QGroupBox("Simulation")
        
        self.render_layout = QtGui.QGridLayout()
        self.render_layout.addWidget(self.render_area)
        self.render_group.setLayout(self.render_layout)
        
        self.controls_group = self.createRobotControls()
        
        layout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        layout.addWidget(self.render_group)
        layout.addWidget(self.controls_group)
        
        self.setLayout(layout)
        self.setWindowTitle(self.tr("Homework 2"))
    
    def minimumSizeHint(self):
        return QtCore.QSize(1000, 600)
    
    def sizeHint(self):
        return QtCore.QSize(1000, 600)
    
    def createRobotControls(self):
        """Creates the robot controls"""
        control_group = QtGui.QGroupBox("Controls")
        control_layout = QtGui.QGridLayout()
        
        self.leftWheelLabel = QtGui.QLabel("Left Wheel")
        
        self.leftWheelSpinBox = QtGui.QSpinBox()
        self.leftWheelSpinBox.setRange(-100, 100)
        self.leftWheelSpinBox.setSingleStep(1)
        
        self.leftWheelSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.leftWheelSlider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.leftWheelSlider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.leftWheelSlider.setRange(-100, 100)
        self.leftWheelSlider.setTickInterval(10)
        self.leftWheelSlider.setSingleStep(1)
        
        self.leftWheelSpinBox.valueChanged[int].connect(self.leftWheelSlider.setValue)
        self.leftWheelSlider.valueChanged[int].connect(self.leftWheelSpinBox.setValue)
        
        control_layout.addWidget(self.leftWheelLabel)
        control_layout.addWidget(self.leftWheelSpinBox)
        control_layout.addWidget(self.leftWheelSlider)
        
        self.rightWheelLabel = QtGui.QLabel("Right Wheel")
        
        self.rightWheelSpinBox = QtGui.QSpinBox()
        self.rightWheelSpinBox.setRange(-100, 100)
        self.rightWheelSpinBox.setSingleStep(1)
        
        self.rightWheelSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.rightWheelSlider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.rightWheelSlider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.rightWheelSlider.setRange(-100, 100)
        self.rightWheelSlider.setTickInterval(10)
        self.rightWheelSlider.setSingleStep(1)
        
        self.rightWheelSpinBox.valueChanged[int].connect(self.rightWheelSlider.setValue)
        self.rightWheelSlider.valueChanged[int].connect(self.rightWheelSpinBox.setValue)
        
        control_layout.addWidget(self.rightWheelLabel)
        control_layout.addWidget(self.rightWheelSpinBox)
        control_layout.addWidget(self.rightWheelSlider)
        
        control_layout.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        control_group.setLayout(control_layout)
        return control_group
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
