#!/usr/bin/env python

import sys
from Queue import Queue

from PySide import QtCore, QtGui

from costmap import Costmap2D
from obstacle import Obstacle
from brushfire import BrushfireExpansion

class CellWidget(QtGui.QLabel):
    """Represents a Cell Widget"""
    def __init__(self, value = 0.0, parent = None):
        QtGui.QLabel.__init__(self, parent=parent)
        self.value = value
        self.text = str(self.value)
    

class Costmap2DWidget(QtGui.QWidget):
    costmap_changed = QtCore.Signal()
    
    """Implements a widget that will display a costmap"""
    def __init__(self, costmap, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.costmap = costmap
        
        self.create_cell_grid()
        
        self.change_queue = Queue()
        self.idle = True
        
        self.connect_stuff()
        
        self.costmap.on_update = self.costmap_update_callback
    
    def create_cell_grid(self):
        """Creates the grid of cells"""
        self.grid_cells = [[None]*self.costmap.height]*self.costmap.width
        self.grid_cells_layout = QtGui.QGridLayout()
        for (x, row) in enumerate(self.costmap):
            for (y, cell_value) in enumerate(row):
                cell = CellWidget(cell_value)
                self.grid_cells[x][y] = cell
                self.grid_cells_layout.addWidget(cell, y, x)
        self.setLayout(self.grid_cells_layout)
    
    def connect_stuff(self):
        """Make Qt connections"""
        self.costmap_changed.connect(self.on_map_update)
    
    def costmap_update_callback(self, key, val):
        """Callback to handle when the map is updated"""
        self.change_queue.put((key, val))
        if self.idle:
            self.idle = False
            self.costmap_changed.emit()
    
    def on_map_update(self):
        """Slot to handle the costmap_changed signal"""
        while not self.change_queue.empty():
            key, val = self.change_queue.get()
            # Do Work
            if slice in [type(key[0]), type(key[1])]:
                print key, val
            self.change_queue.task_done()
        self.idle = True
    

if __name__ == '__main__':
    try:
        c = Costmap2D(10,20,resolution=0.5)
        Obstacle(3,3,3,3).draw(c)
        Obstacle(5,9,3,3).draw(c)
        Obstacle(4,16,3,3).draw(c)
        
        app = QtGui.QApplication(sys.argv)
        cw = Costmap2DWidget(c)
        
        be = BrushfireExpansion(c)
        be.set_ignition_cells([(0,0)])
        be.solve()
        
        import numpy as np
        c[1,1:5] = np.array([-7,-7,-7,-7])
        c[2:6,1] = np.array([-9,-9,-9,-9])
        
        print c
        
        cw.show()
        sys.exit(app.exec_())
    except SystemExit:
        pass
    except:
        import traceback; traceback.print_exc()
