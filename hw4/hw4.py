#!/usr/bin/env python

import sys
from copy import copy

from PySide import QtCore, QtGui

from costmap import Costmap2D
from obstacle import Obstacle
from brushfire import BrushfireExpansion
from costmapwidget import Costmap2DWidget

DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 20
DEFAULT_RESOLUTION = 1.0

class AlgorithmWidget(QtGui.QGroupBox):
    def __init__(self, name="Unnamed Algorithm", parent=None):
        QtGui.QGroupBox.__init__(self, name, parent=parent)
        
        self.costmap = Costmap2D(DEFAULT_WIDTH, DEFAULT_HEIGHT, resolution=DEFAULT_RESOLUTION)
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(5,9,3,3).draw(self.costmap)
        Obstacle(4,16,3,3).draw(self.costmap)
        
        self.costmap_widget = Costmap2DWidget(self.costmap, parent = self)
        
        self.run_button = QtGui.QPushButton("Run")
        self.step_button = QtGui.QPushButton("Step")
        self.reset_button = QtGui.QPushButton("Reset")
        self.buttons = [self.run_button, self.step_button, self.reset_button]
        
        self.make_connections()
    
    def make_connections(self):
        """Makes the Qt connections"""
        self.run_button.clicked.connect(self.on_run_clicked)
    
    @QtCore.Slot()
    def on_run_clicked(self):
        """Called when run is clicked"""
        print '(run button) implement me!'
    
    def pack_buttons(self):
        """Puts the buttons into the layout, this lets additional buttons to be inserted"""
        button_layout = QtGui.QHBoxLayout()
        for button in self.buttons:
            button_layout.addWidget(button)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.costmap_widget)
        layout.addLayout(button_layout)
        layout.addStretch(1)
        self.setLayout(layout)
    

class Homework4App(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        example = AlgorithmWidget(parent=self)
        example.pack_buttons()
        
        layout = QtGui.QHBoxLayout()
        layout.addWidget(example)
        self.setLayout(layout)
    

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    hw4app = Homework4App()
    hw4app.show()
    sys.exit(app.exec_())
