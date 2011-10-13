#!/usr/bin/env python

import sys

from PySide import QtCore, QtGui

from costmap import Costmap2D
from costmapwidget import Costmap2DWidget
from obstacle import Obstacle
from brushfire import BrushfireExpansion
from algorithmwidget import AlgorithmWidget

class BrushfireAlgorithmWidget(AlgorithmWidget):
    def __init__(self, parent = None):
        AlgorithmWidget.__init__(self, "Brushfire Algorithm", parent)
        
        self.pack_buttons()
    
    def setup_algorithm(self):
        """Sets up the algorithm"""
        self.costmap = Costmap2D(DEFAULT_WIDTH, DEFAULT_HEIGHT, resolution=DEFAULT_RESOLUTION)
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(5,9,3,3).draw(self.costmap)
        Obstacle(4,16,3,3).draw(self.costmap)
        
        self.costmap_widget = Costmap2DWidget(self.costmap, parent = self)
        self.be = BrushfireExpansion(self.costmap)
        self.be.set_ignition_cells([self.costmap_widget.start_coord])
    
    def step_solution(self):
        """Steps the solution"""
        pass
    
    def reset_algorithm(self):
        """Resets the algorithm"""
        self.costmap = Costmap2D(DEFAULT_WIDTH, DEFAULT_HEIGHT, resolution=DEFAULT_RESOLUTION)
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(5,9,3,3).draw(self.costmap)
        Obstacle(4,16,3,3).draw(self.costmap)
        
        self.be = BrushfireExpansion(self.costmap)
        self.be.set_ignition_cells([self.costmap_widget.start_coord])
    

class Homework4App(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.algorithms = []
        
        example = AlgorithmWidget(parent=self)
        example.pack_buttons()
        self.algorithms.append(example)
        
        layout = QtGui.QHBoxLayout()
        layout.addWidget(example)
        self.setLayout(layout)
    

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    hw4app = Homework4App()
    hw4app.show()
    sys.exit(app.exec_())
