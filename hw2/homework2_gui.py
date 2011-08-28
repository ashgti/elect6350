#!/usr/bin/env python

import sys
from PySide import QtCore, QtGui
from mainwindow import Ui_MainWindow

from homework2 import DifferentialKinematics

class MainWindow(QtGui.QMainWindow):
    """This is the implementation of the generated UI of the MainWindow"""
    def __init__(self, ui):
        QtGui.QMainWindow.__init__(self)
        self.ui = ui
        
        self.ui.setupUi(self)
        
        self.dk = DifferentialKinematics(0.30, 0.15)
        
        self.connectComponents()
    
    def connectComponents(self):
        """Handles connection of different signals to slots"""
        # self.linear_velocity_changed = QtCore.Signal(int)
        # self.linear_velocity_changed.connect(self.ui.linear_velocity_spinbox.setValue)
        # self.angular_velocity_changed = QtCore.Signal(int)
    
    def onLeftWheelSpeedChanged(self, value):
        """Handle the left wheel speed changing"""
        (l, a) = self.dk.forward(left_wheel_speed = value)
        # self.linear_velocity_changed.emit(l)
        # self.angular_velocity_changed.emit(a)
    
    def onRightWheelSpeedChanged(self, value):
        """Handle the right wheel speed changing"""
        pass
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui_mainwindow = Ui_MainWindow()
    main_window = MainWindow(ui_mainwindow)
    main_window.show()
    sys.exit(app.exec_())
