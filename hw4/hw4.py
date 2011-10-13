#!/usr/bin/env python

import sys
from math import floor

from PySide import QtCore, QtGui

from costmap import Costmap2D
from costmapwidget import Costmap2DWidget
from obstacle import Obstacle
from brushfire import BrushfireExpansion
from algorithmwidget import AlgorithmWidget

DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 20
DEFAULT_RESOLUTION = 0.5

DEFAULT_TIMEOUT = 0.1

class BrushfireAlgorithmWidget(AlgorithmWidget):
    def __init__(self, parent = None, colorbar = False):
        self.colorbar = colorbar
        AlgorithmWidget.__init__(self, "Brushfire Algorithm", parent)
        self.pack_buttons()
    
    def setup_algorithm(self):
        """Sets up the algorithm"""
        # print 'Setting up BE'
        self.costmap = Costmap2D(DEFAULT_WIDTH, DEFAULT_HEIGHT, resolution=DEFAULT_RESOLUTION)
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(5,9,3,3).draw(self.costmap)
        Obstacle(4,16,3,3).draw(self.costmap)
        
        self.costmap_widget = Costmap2DWidget(self.costmap, parent = self, show_goal = False,
                                                show_colorbar = self.colorbar)
        self.costmap_widget.canvas.show_start = True
        self.costmap_widget.canvas.show_goal = False
        self.be = BrushfireExpansion(self.costmap)
        temp = self.costmap_widget.canvas.start_coord
        self.start_coord = (floor(temp[0]+0.5), floor(temp[1]+0.5))
        self.be.set_ignition_cells([self.start_coord])
    
    def step_solution(self):
        """Steps the solution"""
        # print 'Stepping BE'
        result = self.be.step_solution()
        return result
    
    def reset_algorithm(self):
        """Resets the algorithm"""
        # print 'Resetting BE'
        self.costmap_widget.canvas.freeze = True
        self.costmap[:] = 0.0
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(5,9,3,3).draw(self.costmap)
        Obstacle(4,16,3,3).draw(self.costmap)
        
        self.be = BrushfireExpansion(self.costmap)
        temp = self.costmap_widget.canvas.start_coord
        self.start_coord = (floor(temp[0]+0.5), floor(temp[1]+0.5))
        self.be.set_ignition_cells([self.start_coord])
        self.costmap_widget.canvas.freeze = False
        self.costmap_widget.canvas.on_map_update()
    

class Homework4App(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        algorithms = []
        
        algorithms.append(BrushfireAlgorithmWidget(self))
        algorithms.append(BrushfireAlgorithmWidget(self, True))
        
        layout = QtGui.QHBoxLayout()
        for algorithm in algorithms:
            layout.addWidget(algorithm)
        self.setLayout(layout)
    

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    hw4app = Homework4App()
    hw4app.show()
    sys.exit(app.exec_())
