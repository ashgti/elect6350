#!/usr/bin/env python

import sys
from PySide import QtCore, QtGui
from mainwindow import Ui_MainWindow

from homework2 import DifferentialKinematics

class MainWindow(QtGui.QMainWindow):
    """This is the implementation of the generated UI of the MainWindow"""
    
    left_wheel_speed_changed = QtCore.Signal(int)
    right_wheel_speed_changed = QtCore.Signal(int)
    linear_velocity_changed = QtCore.Signal(int)
    angular_velocity_changed = QtCore.Signal(int)
    
    def __init__(self, ui):
        QtGui.QMainWindow.__init__(self)
        self.ui = ui
        
        self.ui.setupUi(self)
        
        self.dk = DifferentialKinematics(0.30, 0.15)
        
        self.connectComponents()
    
    def connectComponents(self):
        """Handles connection of different signals to slots"""
        self.ui.left_wheel_spinbox.valueChanged.connect(self.onLeftWheelSpeedChanged)
        self.ui.right_wheel_spinbox.valueChanged.connect(self.onRightWheelSpeedChanged)
        self.ui.linear_velocity_spinbox.valueChanged.connect(self.onLinearVelocityChanged)
        self.ui.angular_velocity_spinbox.valueChanged.connect(self.onAngularVelocityChanged)
        
        self.left_wheel_speed_changed.connect(self.ui.left_wheel_spinbox.setValue)
        self.right_wheel_speed_changed.connect(self.ui.right_wheel_spinbox.setValue)
        self.linear_velocity_changed.connect(self.ui.linear_velocity_spinbox.setValue)
        self.angular_velocity_changed.connect(self.ui.angular_velocity_spinbox.setValue)
    
    @QtCore.Slot(int)
    def onLeftWheelSpeedChanged(self, value):
        """Handle the left wheel speed changing"""
        (l, a) = self.dk.forward(left_wheel_speed = float(value))
        self.linear_velocity_changed.emit(l)
        self.angular_velocity_changed.emit(a)
    
    @QtCore.Slot(int)
    def onRightWheelSpeedChanged(self, value):
        """Handle the right wheel speed changing"""
        (l, a) = self.dk.forward(right_wheel_speed = float(value))
        self.linear_velocity_changed.emit(l)
        self.angular_velocity_changed.emit(a)
    
    @QtCore.Slot(int)
    def onLinearVelocityChanged(self, value):
        """Handle the linear velocity changing"""
        (l, r) = self.dk.inverse(linear_vel = float(value))
        self.left_wheel_speed_changed.emit(l)
        self.right_wheel_speed_changed.emit(r)
    
    @QtCore.Slot(int)
    def onAngularVelocityChanged(self, value):
        """Handle the angular velocity changing"""
        (l, r) = self.dk.inverse(angular_vel = float(value))
        self.left_wheel_speed_changed.emit(l)
        self.right_wheel_speed_changed.emit(r)
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui_mainwindow = Ui_MainWindow()
    main_window = MainWindow(ui_mainwindow)
    main_window.show()
    sys.exit(app.exec_())
