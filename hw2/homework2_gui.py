#!/usr/bin/env python

import sys
from PySide import QtCore, QtGui
from mainwindow import Ui_MainWindow

from math import radians

have_matplotlib = True
try:
    from plot import PlotWindow
except ImportError:
    have_matplotlib = False

from homework2 import DifferentialKinematics

class MainWindow(QtGui.QMainWindow):
    """This is the implementation of the generated UI of the MainWindow"""
    
    left_wheel_speed_changed = QtCore.Signal(float)
    right_wheel_speed_changed = QtCore.Signal(float)
    linear_velocity_changed = QtCore.Signal(float)
    angular_velocity_changed = QtCore.Signal(float)
    
    def __init__(self, ui):
        QtGui.QMainWindow.__init__(self)
        self.ui = ui
        self.sim_period = 0.1
        self.sim_timer = QtCore.QTimer(self)
        self.sim_timer.timeout.connect(self.simTimeEpoch)
        self.simulation_running = False
        self.current_time = 0.0
        
        self.robot_xs = []
        self.robot_ys = []
        self.robot_ws = []
        self.robot_times = []
        self.graphing = False
        self.plot_window = None
        
        self.ui.setupUi(self)
        
        self.dk = DifferentialKinematics(0.30, 0.15, w=radians(self.ui.render_area.robot_rotation))
        
        self.onLeftWheelSpeedChanged(self.ui.left_wheel_spinbox.value())
        self.onRightWheelSpeedChanged(self.ui.right_wheel_spinbox.value())
        
        self.connectComponents()
    
    def connectComponents(self):
        """Handles connection of different signals to slots"""
        self.ui.left_wheel_spinbox.valueChanged.connect(self.onLeftWheelSpeedChanged)
        self.ui.right_wheel_spinbox.valueChanged.connect(self.onRightWheelSpeedChanged)
        # self.ui.linear_velocity_spinbox.valueChanged.connect(self.onLinearVelocityChanged)
        # self.ui.angular_velocity_spinbox.valueChanged.connect(self.onAngularVelocityChanged)
        
        self.left_wheel_speed_changed.connect(self.ui.left_wheel_spinbox.setValue)
        self.right_wheel_speed_changed.connect(self.ui.right_wheel_spinbox.setValue)
        self.linear_velocity_changed.connect(self.ui.linear_velocity_spinbox.setValue)
        self.angular_velocity_changed.connect(self.ui.angular_velocity_spinbox.setValue)
        
        self.ui.sim_time_slider.valueChanged.connect(self.onSimTimeSliderChanged)
        
        self.ui.toggle_simulation.clicked.connect(self.toggleSimulation)
        self.ui.reset_simulation.clicked.connect(self.reset)
        
        self.ui.graph_button.clicked.connect(self.toggleGraphing)
    
    def simTimeEpoch(self):
        """Handle time update for simulation"""
        self.current_time += self.sim_period
        x,y,w = self.dk.stepSimulation(self.sim_period)
        self.robot_xs.append(x)
        self.robot_ys.append(y)
        self.robot_ws.append(w)
        self.robot_times.append(self.current_time)
        self.updatePlots()
        self.ui.render_area.updateDisplay(x, y, w, self.current_time)
    
    def updatePlots(self):
        """Updates the plt window if graphing"""
        if self.graphing and self.plot_window != None:
            self.plot_window.plotHeading(self.robot_ws, self.robot_times)
    
    def reset(self):
        """Resets the simualtion"""
        if self.simulation_running:
            self.toggleSimulation()
        self.current_time = 0.0
        self.ui.render_area.reset()
        self.dk = DifferentialKinematics(0.30, 0.15,
                    w=radians(self.ui.render_area.robot_rotation))
        l = self.ui.left_wheel_spinbox.value()
        r = self.ui.right_wheel_spinbox.value()
        self.dk.forward(l, r)
    
    def toggleGraphing(self, event=None):
        """Toggles the graphingon robot motion"""
        if not have_matplotlib:
            QtGui.QErrorMessage(self).showMessage("""You don't have matplotlib installed.  
Get it here: http://sourceforge.net/projects/matplotlib/files/matplotlib/""")
            return
        if self.graphing:
            self.graphing = False
            self.plot_window = None
        else:
            self.plot_window = PlotWindow(self)
            # self.plot_window.setWindowFlags(QtCore.Qt.Drawer)
            self.plot_window.setWindowFlags(QtCore.Qt.Tool)
            self.plot_window.show()
            self.graphing = True
    
    def toggleSimulation(self, event=None):
        """Starts the simulation"""
        if self.simulation_running:
            self.ui.toggle_simulation.setText("Start")
            self.sim_timer.stop()
            self.simulation_running = False
        else:
            self.ui.toggle_simulation.setText("Pause")
            self.sim_timer.start(self.sim_period*1000.0)
            self.simulation_running = True
    
    @QtCore.Slot(int)
    def onSimTimeSliderChanged(self, value):
        """Handle the Sim Time slider changing"""
        if value == 1:
            self.sim_period = 0.2
            self.sim_timer.setInterval(self.sim_period*1000.0)
            self.ui.sim_time_label.setText("5 Sim Steps per Second")
        elif value == 2:
            self.sim_period = 0.1
            self.sim_timer.setInterval(self.sim_period*1000.0)
            self.ui.sim_time_label.setText("10 Sim Steps per Second")
        elif value == 3:
            self.sim_period = 0.01
            self.sim_timer.setInterval(self.sim_period*1000.0)
            self.ui.sim_time_label.setText("100 Sim Steps per Second")
    
    @QtCore.Slot(str)
    def onLeftWheelSpeedChanged(self, value):
        """Handle the left wheel speed changing"""
        (l, a) = self.dk.forward(left_wheel_speed = float(value))
        self.linear_velocity_changed.emit(l)
        self.angular_velocity_changed.emit(a)
    
    @QtCore.Slot(str)
    def onRightWheelSpeedChanged(self, value):
        """Handle the right wheel speed changing"""
        (l, a) = self.dk.forward(right_wheel_speed = float(value))
        self.linear_velocity_changed.emit(l)
        self.angular_velocity_changed.emit(a)
    
    @QtCore.Slot(str)
    def onLinearVelocityChanged(self, value):
        """Handle the linear velocity changing"""
        (l, r) = self.dk.inverse(linear_vel = float(value))
        self.left_wheel_speed_changed.emit(l)
        self.right_wheel_speed_changed.emit(r)
    
    @QtCore.Slot(str)
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
